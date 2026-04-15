/**
 * Wiki Storage
 *
 * File I/O layer for the LLM Wiki knowledge base.
 * Standalone version — no OMC dependency.
 *
 * Storage layout:
 *   docs/wiki/
 *   ├── index.md      (auto-maintained catalog)
 *   ├── log.md         (append-only operation chronicle)
 *   ├── page-slug.md   (knowledge pages)
 *   └── ...
 */

import { existsSync, readFileSync, readdirSync, unlinkSync, mkdirSync, writeFileSync } from 'fs';
import { join, resolve, sep } from 'path';
import { WIKI_SCHEMA_VERSION } from './types.mjs';

// ============================================================================
// Constants
// ============================================================================

const INDEX_FILE = 'index.md';
const LOG_FILE = 'log.md';
const ENVIRONMENT_FILE = 'environment.md';
const RESERVED_FILES = new Set([INDEX_FILE, LOG_FILE, ENVIRONMENT_FILE]);

// ============================================================================
// Path helpers
// ============================================================================

/** Get the wiki directory path. Uses WIKI_ROOT env var or defaults to 'docs/wiki'. */
export function getWikiDir(root) {
  const wikiRoot = process.env.WIKI_ROOT || join('docs', 'wiki');
  return join(root, wikiRoot);
}

/** Ensure wiki directory exists. */
export function ensureWikiDir(root) {
  const wikiDir = getWikiDir(root);
  if (!existsSync(wikiDir)) {
    mkdirSync(wikiDir, { recursive: true });
  }
  return wikiDir;
}

// ============================================================================
// Frontmatter Parsing
// ============================================================================

/**
 * Parse YAML frontmatter from markdown content.
 * Expects content starting with `---\n...\n---\n`.
 */
export function parseFrontmatter(raw) {
  const normalized = raw.replace(/\r\n/g, '\n');
  const match = normalized.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return null;

  const yamlBlock = match[1];
  const content = match[2];

  try {
    const fm = parseSimpleYaml(yamlBlock);
    const frontmatter = {
      title: String(fm.title || ''),
      tags: parseYamlArray(fm.tags),
      created: String(fm.created || new Date().toISOString()),
      updated: String(fm.updated || new Date().toISOString()),
      sources: parseYamlArray(fm.sources),
      links: parseYamlArray(fm.links),
      category: fm.category || 'reference',
      confidence: fm.confidence || 'medium',
      schemaVersion: Number(fm.schemaVersion) || WIKI_SCHEMA_VERSION,
    };
    return { frontmatter, content };
  } catch {
    return null;
  }
}

/** Simple YAML parser for frontmatter (key: value pairs, no nesting). */
function parseSimpleYaml(yaml) {
  const result = {};
  for (const line of yaml.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let value = line.slice(colonIdx + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1).replace(/\\(\\|"|n|r)/g, (_, ch) => {
        if (ch === 'n') return '\n';
        if (ch === 'r') return '\r';
        return ch;
      });
    }
    if (key) result[key] = value;
  }
  return result;
}

/** Parse YAML array: [item1, item2] or bare string → string[]. */
function parseYamlArray(value) {
  if (!value) return [];
  const trimmed = value.trim();
  if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
    return trimmed
      .slice(1, -1)
      .split(',')
      .map(s => s.trim().replace(/^["']|["']$/g, '').replace(/\\(\\|"|n|r)/g, (_, ch) => {
        if (ch === 'n') return '\n';
        if (ch === 'r') return '\r';
        return ch;
      }))
      .filter(Boolean);
  }
  return trimmed ? [trimmed] : [];
}

/** Escape a string for use inside YAML double quotes. */
function escapeYaml(s) {
  return s.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r');
}

/**
 * Serialize frontmatter + content to markdown string.
 */
export function serializePage(page) {
  const fm = page.frontmatter;
  const yaml = [
    `title: "${escapeYaml(fm.title)}"`,
    `tags: [${fm.tags.map(t => `"${escapeYaml(t)}"`).join(', ')}]`,
    `created: ${fm.created}`,
    `updated: ${fm.updated}`,
    `sources: [${fm.sources.map(s => `"${escapeYaml(s)}"`).join(', ')}]`,
    `links: [${fm.links.map(l => `"${escapeYaml(l)}"`).join(', ')}]`,
    `category: ${fm.category}`,
    `confidence: ${fm.confidence}`,
    `schemaVersion: ${fm.schemaVersion}`,
  ].join('\n');

  return `---\n${yaml}\n---\n${page.content}`;
}

// ============================================================================
// Path Security
// ============================================================================

function safeWikiPath(wikiDir, filename) {
  if (filename.includes('/') || filename.includes('\\') || filename.includes('..')) {
    return null;
  }
  const filePath = join(wikiDir, filename);
  const resolved = resolve(filePath);
  if (!resolved.startsWith(resolve(wikiDir) + sep)) {
    return null;
  }
  return filePath;
}

// ============================================================================
// Read Operations
// ============================================================================

/** Read a single wiki page by filename. */
export function readPage(root, filename) {
  const wikiDir = getWikiDir(root);
  const filePath = safeWikiPath(wikiDir, filename);
  if (!filePath) return null;
  if (!existsSync(filePath)) return null;

  try {
    const raw = readFileSync(filePath, 'utf-8');
    const parsed = parseFrontmatter(raw);
    if (!parsed) return null;
    return { filename, frontmatter: parsed.frontmatter, content: parsed.content };
  } catch {
    return null;
  }
}

/** List all wiki page filenames (excluding reserved files). */
export function listPages(root) {
  const wikiDir = getWikiDir(root);
  if (!existsSync(wikiDir)) return [];
  return readdirSync(wikiDir)
    .filter(f => f.endsWith('.md') && !RESERVED_FILES.has(f))
    .sort();
}

/** Read all wiki pages. */
export function readAllPages(root) {
  return listPages(root)
    .map(f => readPage(root, f))
    .filter(p => p !== null);
}

/** Read index.md content. */
export function readIndex(root) {
  const indexPath = join(getWikiDir(root), INDEX_FILE);
  if (!existsSync(indexPath)) return null;
  return readFileSync(indexPath, 'utf-8');
}

/** Read log.md content. */
export function readLog(root) {
  const logPath = join(getWikiDir(root), LOG_FILE);
  if (!existsSync(logPath)) return null;
  return readFileSync(logPath, 'utf-8');
}

// ============================================================================
// Write Operations
// ============================================================================

/** Write a wiki page to disk. */
export function writePage(root, page) {
  if (RESERVED_FILES.has(page.filename)) {
    throw new Error(`Cannot write to reserved wiki file: ${page.filename}`);
  }
  const wikiDir = ensureWikiDir(root);
  const filePath = safeWikiPath(wikiDir, page.filename);
  if (!filePath) throw new Error(`Invalid wiki page filename: ${page.filename}`);
  writeFileSync(filePath, serializePage(page), 'utf-8');
  updateIndex(root);
}

/** Delete a wiki page. */
export function deletePage(root, filename) {
  const wikiDir = getWikiDir(root);
  const filePath = safeWikiPath(wikiDir, filename);
  if (!filePath) return false;
  if (!existsSync(filePath)) return false;
  unlinkSync(filePath);
  updateIndex(root);
  return true;
}

/**
 * Regenerate index.md from all pages.
 */
export function updateIndex(root) {
  const pages = readAllPages(root);
  const byCategory = new Map();

  for (const page of pages) {
    const cat = page.frontmatter.category;
    if (!byCategory.has(cat)) byCategory.set(cat, []);
    byCategory.get(cat).push(page);
  }

  const lines = [
    '# Wiki Index',
    '',
    `> ${pages.length} pages | Last updated: ${new Date().toISOString()}`,
    '',
  ];

  const sortedCategories = [...byCategory.keys()].sort();
  for (const cat of sortedCategories) {
    lines.push(`## ${cat}`);
    lines.push('');
    for (const page of byCategory.get(cat)) {
      const summary = page.content.split('\n').find(l => l.trim().length > 0)?.trim() || '';
      const truncated = summary.length > 80 ? summary.slice(0, 77) + '...' : summary;
      lines.push(`- [${page.frontmatter.title}](${page.filename}) — ${truncated}`);
    }
    lines.push('');
  }

  const wikiDir = ensureWikiDir(root);
  writeFileSync(join(wikiDir, INDEX_FILE), lines.join('\n'), 'utf-8');
}

/** Append a log entry to log.md. */
export function appendLog(root, entry) {
  const wikiDir = ensureWikiDir(root);
  const logPath = join(wikiDir, LOG_FILE);

  const logLine = `## [${entry.timestamp}] ${entry.operation}\n` +
    `- **Pages:** ${entry.pagesAffected.join(', ') || 'none'}\n` +
    `- **Summary:** ${entry.summary}\n\n`;

  let existing = '';
  if (existsSync(logPath)) {
    existing = readFileSync(logPath, 'utf-8');
  } else {
    existing = '# Wiki Log\n\n';
  }

  writeFileSync(logPath, existing + logLine, 'utf-8');
}

// ============================================================================
// Slug Utilities
// ============================================================================

/** Convert a title to a filename slug. */
export function titleToSlug(title) {
  const base = title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 64);

  if (!base) {
    // Non-ASCII-only titles (CJK, Hangul, etc.) produce an empty base.
    // Generate a deterministic hash-based fallback.
    let hash = 0;
    for (let i = 0; i < title.length; i++) {
      hash = ((hash << 5) - hash + title.charCodeAt(i)) | 0;
    }
    return `page-${Math.abs(hash).toString(16).padStart(8, '0')}.md`;
  }

  return `${base}.md`;
}
