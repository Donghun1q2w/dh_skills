/**
 * Wiki Lint
 *
 * Health checks for the wiki knowledge base.
 * Detects orphan pages, stale content, broken cross-references,
 * oversized pages, and structural contradictions.
 */

import { DEFAULT_WIKI_CONFIG } from './types.mjs';
import { readAllPages, appendLog } from './storage.mjs';

/**
 * Run health checks on the wiki.
 *
 * @param {string} root - Project root directory
 * @param {object} [config] - Wiki configuration (uses defaults if not provided)
 * @returns {{ issues: Array, stats: object }}
 */
export function lintWiki(root, config = DEFAULT_WIKI_CONFIG) {
  const pages = readAllPages(root);
  const issues = [];
  const pageFilenames = new Set(pages.map(p => p.filename));

  // Build incoming link map
  const incomingLinks = new Map();
  for (const page of pages) {
    for (const link of page.frontmatter.links) {
      if (!incomingLinks.has(link)) incomingLinks.set(link, new Set());
      incomingLinks.get(link).add(page.filename);
    }
  }

  const now = Date.now();
  const staleThresholdMs = config.staleDays * 24 * 60 * 60 * 1000;

  for (const page of pages) {
    // 1. Orphan detection
    if (!incomingLinks.has(page.filename) || incomingLinks.get(page.filename).size === 0) {
      issues.push({
        page: page.filename,
        severity: 'info',
        type: 'orphan',
        message: `No other pages link to "${page.frontmatter.title}"`,
      });
    }

    // 2. Stale detection
    const updatedAt = new Date(page.frontmatter.updated).getTime();
    if (now - updatedAt > staleThresholdMs) {
      const daysSince = Math.floor((now - updatedAt) / (24 * 60 * 60 * 1000));
      issues.push({
        page: page.filename,
        severity: 'warning',
        type: 'stale',
        message: `"${page.frontmatter.title}" not updated in ${daysSince} days`,
      });
    }

    // 3. Broken cross-references
    for (const link of page.frontmatter.links) {
      if (!pageFilenames.has(link)) {
        issues.push({
          page: page.filename,
          severity: 'error',
          type: 'broken-ref',
          message: `Broken link to "${link}" from "${page.frontmatter.title}"`,
        });
      }
    }

    // 4. Low confidence
    if (page.frontmatter.confidence === 'low') {
      issues.push({
        page: page.filename,
        severity: 'info',
        type: 'low-confidence',
        message: `"${page.frontmatter.title}" has low confidence — consider verifying or removing`,
      });
    }

    // 5. Oversized pages
    const contentSize = Buffer.byteLength(page.content, 'utf-8');
    if (contentSize > config.maxPageSize) {
      const sizeKB = (contentSize / 1024).toFixed(1);
      issues.push({
        page: page.filename,
        severity: 'warning',
        type: 'oversized',
        message: `"${page.frontmatter.title}" is ${sizeKB}KB — consider splitting into smaller pages`,
      });
    }
  }

  // 6. Structural contradictions
  detectStructuralContradictions(pages, issues);

  const stats = {
    totalPages: pages.length,
    orphanCount: issues.filter(i => i.type === 'orphan').length,
    staleCount: issues.filter(i => i.type === 'stale').length,
    brokenRefCount: issues.filter(i => i.type === 'broken-ref').length,
    lowConfidenceCount: issues.filter(i => i.type === 'low-confidence').length,
    oversizedCount: issues.filter(i => i.type === 'oversized').length,
    contradictionCount: issues.filter(i => i.type === 'structural-contradiction').length,
  };

  appendLog(root, {
    timestamp: new Date().toISOString(),
    operation: 'lint',
    pagesAffected: [...new Set(issues.map(i => i.page))],
    summary: `Lint: ${issues.length} issues (${stats.orphanCount} orphan, ${stats.staleCount} stale, ${stats.brokenRefCount} broken, ${stats.contradictionCount} contradictions)`,
  });

  return { issues, stats };
}

function detectStructuralContradictions(pages, issues) {
  const slugGroups = new Map();
  for (const page of pages) {
    const prefix = page.filename.split('-').slice(0, 2).join('-');
    if (!slugGroups.has(prefix)) slugGroups.set(prefix, []);
    slugGroups.get(prefix).push(page);
  }

  for (const [_prefix, group] of slugGroups) {
    if (group.length < 2) continue;

    const confidences = new Set(group.map(p => p.frontmatter.confidence));
    if (confidences.size > 1 && confidences.has('high') && confidences.has('low')) {
      const titles = group.map(p => `"${p.frontmatter.title}"`).join(', ');
      issues.push({
        page: group[0].filename,
        severity: 'warning',
        type: 'structural-contradiction',
        message: `Conflicting confidence levels for related pages: ${titles}`,
      });
    }

    const tagCategoryPairs = new Map();
    for (const page of group) {
      for (const tag of page.frontmatter.tags) {
        if (!tagCategoryPairs.has(tag)) tagCategoryPairs.set(tag, new Set());
        tagCategoryPairs.get(tag).add(page.frontmatter.category);
      }
    }

    for (const [tag, categories] of tagCategoryPairs) {
      if (categories.size > 1) {
        issues.push({
          page: group[0].filename,
          severity: 'info',
          type: 'structural-contradiction',
          message: `Tag "${tag}" appears in pages with different categories: ${[...categories].join(', ')}`,
        });
        break;
      }
    }
  }
}
