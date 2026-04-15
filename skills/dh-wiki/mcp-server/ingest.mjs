/**
 * Wiki Ingest
 *
 * Processes knowledge into wiki pages. A single ingest can create a new page
 * or merge into an existing one (append strategy — never replaces content).
 */

import { WIKI_SCHEMA_VERSION } from './types.mjs';
import {
  readPage,
  writePage,
  appendLog,
  titleToSlug,
} from './storage.mjs';

/**
 * Ingest knowledge into the wiki.
 *
 * If a page with the same slug exists, merges content (append strategy):
 * - Tags: union of existing + new
 * - Sources: append new sources
 * - Confidence: keep higher level
 * - Content: append as new timestamped section (never replace)
 *
 * @param {string} root - Project root directory
 * @param {object} input - Knowledge to ingest
 * @returns {{ created: string[], updated: string[], totalAffected: number }}
 */
export function ingestKnowledge(root, input) {
  const slug = titleToSlug(input.title);
  const now = new Date().toISOString();
  const result = { created: [], updated: [], totalAffected: 0 };

  const existing = readPage(root, slug);

  if (existing) {
    const merged = mergePage(existing, input, now);
    writePage(root, merged);
    result.updated.push(slug);
  } else {
    const page = createPage(slug, input, now);
    writePage(root, page);
    result.created.push(slug);
  }

  appendLog(root, {
    timestamp: now,
    operation: 'ingest',
    pagesAffected: [...result.created, ...result.updated],
    summary: existing
      ? `Updated "${input.title}" with new content`
      : `Created new page "${input.title}"`,
  });

  result.totalAffected = result.created.length + result.updated.length;
  return result;
}

/** Create a new wiki page from ingest input. */
function createPage(slug, input, now) {
  return {
    filename: slug,
    frontmatter: {
      title: input.title,
      tags: [...new Set(input.tags)],
      created: now,
      updated: now,
      sources: input.sources || [],
      links: extractWikiLinks(input.content),
      category: input.category,
      confidence: input.confidence || 'medium',
      schemaVersion: WIKI_SCHEMA_VERSION,
    },
    content: `\n# ${input.title}\n\n${input.content}\n`,
  };
}

/**
 * Merge new content into an existing page (append strategy).
 */
function mergePage(existing, input, now) {
  const mergedTags = [...new Set([...existing.frontmatter.tags, ...input.tags])];
  const mergedSources = [...new Set([...existing.frontmatter.sources, ...(input.sources || [])])];
  const mergedLinks = [...new Set([
    ...existing.frontmatter.links,
    ...extractWikiLinks(input.content),
  ])];

  const confidenceRank = { high: 3, medium: 2, low: 1 };
  const existingRank = confidenceRank[existing.frontmatter.confidence] || 2;
  const newRank = confidenceRank[input.confidence || 'medium'] || 2;
  const mergedConfidence = newRank >= existingRank
    ? (input.confidence || 'medium')
    : existing.frontmatter.confidence;

  const appendedContent = existing.content.trimEnd() +
    `\n\n---\n\n## Update (${now})\n\n${input.content}\n`;

  return {
    filename: existing.filename,
    frontmatter: {
      ...existing.frontmatter,
      tags: mergedTags,
      updated: now,
      sources: mergedSources,
      links: mergedLinks,
      confidence: mergedConfidence,
    },
    content: appendedContent,
  };
}

/** Extract [[wiki-link]] references from content. */
function extractWikiLinks(content) {
  const matches = content.match(/\[\[([^\]]+)\]\]/g);
  if (!matches) return [];
  return [...new Set(matches.map(m => {
    const name = m.slice(2, -2).trim();
    return titleToSlug(name);
  }))];
}
