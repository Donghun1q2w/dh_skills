#!/usr/bin/env node

/**
 * Wiki MD-Mirror Hook
 *
 * Mirrors arbitrary *.md files in the project to docs/wiki/ pages.
 * Registered on two events for full coverage:
 *   - PostToolUse(Edit|Write|MultiEdit): immediate per-tool sync via tool_input.file_path
 *   - Stop:                              end-of-turn safety net via `git status` scan
 *                                        (catches Bash rm, external editor changes, etc.)
 *
 * Exclusions (any one disqualifies a path):
 *  - docs/plans/**
 *  - docs/revisions/**
 *  - *history.md (any depth)
 *  - docs/wiki/** (prevent self-loop)
 *  - any path segment starting with '.' (.git/, .omc/, .obsidian/, .claude/, ...)
 *  - node_modules/**
 *
 * Write strategy: overwrite (storage.writePage) — not ingest's append-merge,
 * so the mirrored page always reflects the current source file.
 */

import { existsSync, readFileSync } from 'fs';
import { join, relative, basename, isAbsolute } from 'path';
import { pathToFileURL } from 'url';
import { execSync } from 'child_process';

// ─── stdio helpers ─────────────────────────────────────────────────────────

function readStdin(timeoutMs = 1500) {
  return new Promise((resolve) => {
    let data = '';
    const timer = setTimeout(() => resolve(data), timeoutMs);
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => { clearTimeout(timer); resolve(data); });
  });
}

function reply(obj) {
  console.log(JSON.stringify(obj));
}

function bail(suppress = true) {
  reply({ continue: true, suppressOutput: suppress });
}

// ─── path filtering ────────────────────────────────────────────────────────

function toRelPosix(root, abs) {
  const rel = isAbsolute(abs) ? relative(root, abs) : abs;
  return rel.split(/[\\/]+/).join('/');
}

function isExcluded(relPosix) {
  if (!relPosix || relPosix.startsWith('..')) return true;
  const segments = relPosix.split('/');
  if (segments.some((s) => s.startsWith('.'))) return true;
  if (segments.includes('node_modules')) return true;
  if (relPosix.startsWith('docs/plans/')) return true;
  if (relPosix.startsWith('docs/revisions/')) return true;
  if (relPosix.startsWith('docs/wiki/')) return true;
  const name = segments[segments.length - 1];
  if (!name.toLowerCase().endsWith('.md')) return true;
  if (/history\.md$/i.test(name)) return true;
  return false;
}

// ─── payload normalization ─────────────────────────────────────────────────

function extractChangesFromPayload(data) {
  const out = [];
  if (Array.isArray(data?.changes)) {
    for (const c of data.changes) {
      if (c?.path) out.push({ path: c.path, kind: c.kind || c.event || 'modify' });
    }
  }
  if (Array.isArray(data?.paths)) {
    for (const p of data.paths) out.push({ path: p, kind: 'modify' });
  }
  if (typeof data?.file_path === 'string') {
    out.push({ path: data.file_path, kind: 'modify' });
  }
  if (typeof data?.tool_input?.file_path === 'string') {
    out.push({ path: data.tool_input.file_path, kind: 'modify' });
  }
  return out;
}

function gitScanChanges(root) {
  const out = [];
  try {
    const stdout = execSync('git status --porcelain', {
      cwd: root,
      encoding: 'utf-8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    for (const rawLine of stdout.split('\n')) {
      if (!rawLine.trim()) continue;
      const code = rawLine.slice(0, 2);
      let pathPart = rawLine.slice(3);
      if (pathPart.includes(' -> ')) pathPart = pathPart.split(' -> ')[1];
      pathPart = pathPart.trim().replace(/^"|"$/g, '');
      if (!pathPart.toLowerCase().endsWith('.md')) continue;
      const kind = (code.includes('D')) ? 'delete' : 'modify';
      out.push({ path: pathPart, kind });
    }
  } catch { /* not a git repo or git unavailable */ }
  return out;
}

function inferKind(absPath, declaredKind) {
  if (declaredKind === 'delete' || declaredKind === 'deleted' || declaredKind === 'removed') {
    return 'delete';
  }
  return existsSync(absPath) ? 'upsert' : 'delete';
}

// ─── mirroring ─────────────────────────────────────────────────────────────

function shortHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
  }
  return Math.abs(hash).toString(16).padStart(8, '0').slice(0, 6);
}

function buildMirrorTitle(relPosix) {
  const stem = basename(relPosix, '.md');
  const hash = shortHash(relPosix);
  return `${stem} (${hash})`;
}

function mirrorUpsert(storage, root, absPath, relPosix) {
  let raw;
  try { raw = readFileSync(absPath, 'utf-8'); }
  catch { return; }

  const parentDir = relPosix.split('/').slice(-2, -1)[0] || 'root';
  const title = buildMirrorTitle(relPosix);
  const filename = storage.titleToSlug(title);
  const now = new Date().toISOString();
  const existing = storage.readPage(root, filename);
  const created = existing ? existing.frontmatter.created : now;

  const page = {
    filename,
    frontmatter: {
      title,
      tags: ['mirrored', parentDir],
      created,
      updated: now,
      sources: [relPosix],
      links: [],
      category: 'reference',
      confidence: 'medium',
      schemaVersion: 1,
    },
    content: `\n# ${title}\n\n${raw}\n`,
  };

  storage.writePage(root, page);
  storage.appendLog(root, {
    timestamp: now,
    operation: existing ? 'update' : 'create',
    pagesAffected: [filename],
    summary: `Auto-mirror: ${existing ? 'updated' : 'created'} page for ${relPosix}`,
  });
}

function mirrorDelete(storage, root, relPosix) {
  const filename = storage.titleToSlug(buildMirrorTitle(relPosix));
  if (storage.deletePage(root, filename)) {
    storage.appendLog(root, {
      timestamp: new Date().toISOString(),
      operation: 'delete',
      pagesAffected: [filename],
      summary: `Auto-mirror: removed page for deleted ${relPosix}`,
    });
  }
}

/**
 * Sweep mirrored wiki pages whose `sources` no longer exist on disk.
 * Catches the case of untracked source files being deleted — git status
 * does not report those, so we reconcile against the wiki itself.
 */
function sweepOrphans(storage, root) {
  let pages;
  try { pages = storage.readAllPages(root); }
  catch { return; }

  for (const page of pages) {
    const tags = page.frontmatter.tags || [];
    if (!tags.includes('mirrored')) continue;
    const source = (page.frontmatter.sources || [])[0];
    if (!source) continue;
    const sourceAbs = join(root, source);
    if (existsSync(sourceAbs)) continue;
    try {
      if (storage.deletePage(root, page.filename)) {
        storage.appendLog(root, {
          timestamp: new Date().toISOString(),
          operation: 'delete',
          pagesAffected: [page.filename],
          summary: `Auto-mirror: swept orphan page (source ${source} gone)`,
        });
      }
    } catch (error) {
      console.error(`[dh-wiki-file-changed] orphan sweep failed for ${page.filename}:`, error.message);
    }
  }
}

// ─── main ──────────────────────────────────────────────────────────────────

async function main() {
  const input = await readStdin();
  let data;
  try { data = JSON.parse(input || '{}'); }
  catch { bail(); return; }

  const root = data.cwd || process.cwd();
  const eventName = data.hook_event_name || '';

  let changes = extractChangesFromPayload(data);

  if (changes.length === 0 && (eventName === 'Stop' || eventName === '')) {
    changes = gitScanChanges(root);
  }

  if (changes.length === 0) { bail(); return; }

  let storage;
  try {
    const storageUrl = pathToFileURL(
      join(root, 'skills', 'dh-wiki', 'mcp-server', 'storage.mjs')
    ).href;
    storage = await import(storageUrl);
  } catch (error) {
    console.error('[dh-wiki-file-changed] Cannot load storage module:', error.message);
    bail();
    return;
  }

  const processed = new Set();
  for (const { path: rawPath, kind: declaredKind } of changes) {
    const abs = isAbsolute(rawPath) ? rawPath : join(root, rawPath);
    const rel = toRelPosix(root, abs);
    if (processed.has(rel)) continue;
    processed.add(rel);
    if (isExcluded(rel)) continue;

    const kind = inferKind(abs, declaredKind);
    try {
      if (kind === 'delete') {
        mirrorDelete(storage, root, rel);
      } else {
        mirrorUpsert(storage, root, abs, rel);
      }
    } catch (error) {
      console.error(`[dh-wiki-file-changed] mirror failed for ${rel}:`, error.message);
    }
  }

  if (eventName === 'Stop' || eventName === '') {
    sweepOrphans(storage, root);
  }

  bail();
}

main();
