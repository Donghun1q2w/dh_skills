#!/usr/bin/env node

/**
 * Wiki FileChanged Hook
 *
 * Mirrors arbitrary *.md files in the project to docs/wiki/ pages.
 *
 * Exclusions:
 *  - docs/plans/**
 *  - docs/revisions/**
 *  - *history.md (any depth)
 *  - docs/wiki/** (prevent self-loop)
 *  - any path segment starting with '.' (.git/, .omc/, .obsidian/, .claude/, ...)
 *  - node_modules/**
 *
 * On create/modify: ingest mirrored content as a wiki page.
 * On delete:         delete the corresponding wiki page.
 *
 * stdin JSON schema (FileChanged) is not officially documented; this script
 * tries multiple known shapes:
 *   data.file_path                        (string)
 *   data.paths                            (string[])
 *   data.tool_input.file_path             (PostToolUse-like fallback)
 *   data.changes[].path + data.changes[].kind
 */

import {
  existsSync,
  readFileSync,
  statSync,
} from 'fs';
import { join, relative, basename, isAbsolute, sep } from 'path';
import { pathToFileURL } from 'url';

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

function extractChanges(data) {
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

/**
 * Build the wiki title for a mirrored file. Uses file stem + path hash so
 * upsert and delete derive the same slug from the same source path.
 */
function buildMirrorTitle(relPosix) {
  const stem = basename(relPosix, '.md');
  const hash = shortHash(relPosix);
  return `${stem} (${hash})`;
}

async function mirrorUpsert(storage, ingest, root, absPath, relPosix) {
  let raw;
  try { raw = readFileSync(absPath, 'utf-8'); }
  catch { return; }

  const parentDir = relPosix.split('/').slice(-2, -1)[0] || 'root';

  ingest.ingestKnowledge(root, {
    title: buildMirrorTitle(relPosix),
    content: raw,
    tags: ['mirrored', parentDir],
    category: 'reference',
    sources: [relPosix],
    confidence: 'medium',
  });
}

async function mirrorDelete(storage, root, relPosix) {
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

// ─── main ──────────────────────────────────────────────────────────────────

async function main() {
  const input = await readStdin();
  let data;
  try { data = JSON.parse(input || '{}'); }
  catch { bail(); return; }

  const root = data.cwd || process.cwd();

  const changes = extractChanges(data);
  if (changes.length === 0) { bail(); return; }

  let storage, ingest;
  try {
    const storageUrl = pathToFileURL(
      join(root, 'skills', 'dh-wiki', 'mcp-server', 'storage.mjs')
    ).href;
    const ingestUrl = pathToFileURL(
      join(root, 'skills', 'dh-wiki', 'mcp-server', 'ingest.mjs')
    ).href;
    storage = await import(storageUrl);
    ingest = await import(ingestUrl);
  } catch (error) {
    console.error('[dh-wiki-file-changed] Cannot load mcp-server modules:', error.message);
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
        await mirrorDelete(storage, root, rel);
      } else {
        await mirrorUpsert(storage, ingest, root, abs, rel);
      }
    } catch (error) {
      console.error(`[dh-wiki-file-changed] mirror failed for ${rel}:`, error.message);
    }
  }

  bail();
}

main();
