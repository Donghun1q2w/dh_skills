#!/usr/bin/env node

/**
 * dh-wiki MCP Server
 *
 * Standalone LLM Wiki MCP server providing 7 tools:
 * dh_wiki_add, dh_wiki_ingest, dh_wiki_query, dh_wiki_list, dh_wiki_read, dh_wiki_delete, dh_wiki_lint
 *
 * Storage: docs/wiki/ (configurable via WIKI_ROOT env var)
 * Transport: stdio
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { ingestKnowledge } from './ingest.mjs';
import { queryWiki } from './query.mjs';
import { lintWiki } from './lint.mjs';
import {
  readPage,
  listPages,
  readIndex,
  deletePage,
  appendLog,
  titleToSlug,
} from './storage.mjs';
import { WIKI_CATEGORIES } from './types.mjs';

const server = new McpServer({
  name: 'dh-wiki',
  version: '1.0.0',
});

const categoryEnum = z.enum(WIKI_CATEGORIES);

function getRoot() {
  return process.env.PROJECT_ROOT || process.cwd();
}

// ============================================================================
// dh_wiki_ingest
// ============================================================================

server.tool(
  'dh_wiki_ingest',
  'Process knowledge into wiki pages. Creates new pages or merges into existing ones (append strategy — never replaces).',
  {
    title: z.string().max(200).describe('Page title (max 200 chars)'),
    content: z.string().max(50000).describe('Markdown content to ingest (max 50KB)'),
    tags: z.array(z.string().max(50)).max(20).describe('Searchable tags (max 20)'),
    category: categoryEnum.describe('Page category'),
    sources: z.array(z.string().max(100)).max(10).optional().describe('Source identifiers'),
    confidence: z.enum(['high', 'medium', 'low']).optional().describe('Confidence level'),
  },
  async (args) => {
    try {
      const result = ingestKnowledge(getRoot(), {
        title: args.title,
        content: args.content,
        tags: args.tags,
        category: args.category,
        sources: args.sources,
        confidence: args.confidence,
      });
      return {
        content: [{
          type: 'text',
          text: `Wiki ingest complete.\n- Created: ${result.created.join(', ') || 'none'}\n- Updated: ${result.updated.join(', ') || 'none'}\n- Total affected: ${result.totalAffected}`,
        }],
      };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// dh_wiki_query
// ============================================================================

server.tool(
  'dh_wiki_query',
  'Search across all wiki pages by keywords and tags. Returns matching pages with relevance snippets. YOU synthesize answers with citations.',
  {
    query: z.string().describe('Search text'),
    tags: z.array(z.string()).optional().describe('Filter by tags (OR match)'),
    category: categoryEnum.optional().describe('Filter by category'),
    limit: z.number().int().min(1).max(50).optional().describe('Max results (default: 20)'),
  },
  async (args) => {
    try {
      const matches = queryWiki(getRoot(), args.query, {
        tags: args.tags,
        category: args.category,
        limit: args.limit,
      });

      if (matches.length === 0) {
        return { content: [{ type: 'text', text: `No wiki pages match "${args.query}".` }] };
      }

      const results = matches.map((m, i) => {
        const fm = m.page.frontmatter;
        return `### ${i + 1}. ${fm.title} (${fm.category}, ${fm.confidence})\n` +
          `**File:** ${m.page.filename} | **Tags:** ${fm.tags.join(', ')} | **Score:** ${m.score}\n` +
          `**Snippet:** ${m.snippet}`;
      });

      return {
        content: [{
          type: 'text',
          text: `## Wiki Query: "${args.query}"\n\n${matches.length} results:\n\n${results.join('\n\n')}`,
        }],
      };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// dh_wiki_lint
// ============================================================================

server.tool(
  'dh_wiki_lint',
  'Run health checks on the wiki. Detects orphan pages, stale content, broken cross-references, oversized pages.',
  {},
  async () => {
    try {
      const report = lintWiki(getRoot());

      if (report.issues.length === 0) {
        return { content: [{ type: 'text', text: `Wiki lint: ${report.stats.totalPages} pages, no issues found.` }] };
      }

      const issueLines = report.issues.map(i =>
        `- [${i.severity.toUpperCase()}] ${i.type}: ${i.message}`
      );

      return {
        content: [{
          type: 'text',
          text: `## Wiki Lint Report\n\n` +
            `**${report.stats.totalPages} pages**, ${report.issues.length} issues:\n\n` +
            issueLines.join('\n') +
            `\n\n**Summary:** ${report.stats.orphanCount} orphan, ${report.stats.staleCount} stale, ` +
            `${report.stats.brokenRefCount} broken refs, ${report.stats.contradictionCount} contradictions, ` +
            `${report.stats.oversizedCount} oversized`,
        }],
      };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// dh_wiki_add
// ============================================================================

server.tool(
  'dh_wiki_add',
  'Quick-add a wiki page. Simpler than dh_wiki_ingest — creates a single page directly.',
  {
    title: z.string().max(200).describe('Page title (max 200 chars)'),
    content: z.string().max(50000).describe('Page content in markdown (max 50KB)'),
    tags: z.array(z.string().max(50)).max(20).optional().describe('Tags (default: [])'),
    category: categoryEnum.optional().describe('Category (default: reference)'),
  },
  async (args) => {
    try {
      const root = getRoot();
      const slug = titleToSlug(args.title);

      if (readPage(root, slug)) {
        return {
          content: [{ type: 'text', text: `Page "${slug}" already exists. Use dh_wiki_ingest to merge content.` }],
          isError: true,
        };
      }

      const result = ingestKnowledge(root, {
        title: args.title,
        content: args.content,
        tags: args.tags || [],
        category: args.category || 'reference',
      });

      return {
        content: [{ type: 'text', text: `Wiki page created: ${result.created[0]}\nPath: docs/wiki/${result.created[0]}` }],
      };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// dh_wiki_list
// ============================================================================

server.tool(
  'dh_wiki_list',
  'List all wiki pages with summaries. Reads the auto-maintained index.',
  {},
  async () => {
    try {
      const root = getRoot();
      const index = readIndex(root);

      if (!index) {
        const pages = listPages(root);
        if (pages.length === 0) {
          return { content: [{ type: 'text', text: 'Wiki is empty. Use dh_wiki_add or dh_wiki_ingest to create pages.' }] };
        }
        return { content: [{ type: 'text', text: `Wiki has ${pages.length} pages but no index.\n${pages.map(p => `- ${p}`).join('\n')}` }] };
      }

      return { content: [{ type: 'text', text: index }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// dh_wiki_read
// ============================================================================

server.tool(
  'dh_wiki_read',
  'Read a specific wiki page by filename (without .md extension is OK).',
  {
    page: z.string().describe('Page filename or slug (e.g., "auth-architecture")'),
  },
  async (args) => {
    try {
      const filename = args.page.endsWith('.md') ? args.page : `${args.page}.md`;
      const page = readPage(getRoot(), filename);

      if (!page) {
        return { content: [{ type: 'text', text: `Wiki page not found: ${filename}` }], isError: true };
      }

      const fm = page.frontmatter;
      const header = [
        `## ${fm.title}`,
        `**Category:** ${fm.category} | **Confidence:** ${fm.confidence} | **Updated:** ${fm.updated}`,
        `**Tags:** ${fm.tags.join(', ')}`,
        fm.links.length > 0 ? `**Links:** ${fm.links.join(', ')}` : '',
        fm.sources.length > 0 ? `**Sources:** ${fm.sources.join(', ')}` : '',
        '',
      ].filter(Boolean).join('\n');

      return { content: [{ type: 'text', text: `${header}\n${page.content}` }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// dh_wiki_delete
// ============================================================================

server.tool(
  'dh_wiki_delete',
  'Delete a wiki page by filename.',
  {
    page: z.string().describe('Page filename or slug to delete'),
  },
  async (args) => {
    try {
      const root = getRoot();
      const filename = args.page.endsWith('.md') ? args.page : `${args.page}.md`;
      const deleted = deletePage(root, filename);

      if (!deleted) {
        return { content: [{ type: 'text', text: `Wiki page not found: ${filename}` }], isError: true };
      }

      appendLog(root, {
        timestamp: new Date().toISOString(),
        operation: 'delete',
        pagesAffected: [filename],
        summary: `Deleted page "${filename}"`,
      });

      return { content: [{ type: 'text', text: `Deleted wiki page: ${filename}` }] };
    } catch (error) {
      return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
    }
  }
);

// ============================================================================
// Start server
// ============================================================================

const transport = new StdioServerTransport();
await server.connect(transport);
