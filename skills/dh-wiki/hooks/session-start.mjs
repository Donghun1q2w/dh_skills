#!/usr/bin/env node

/**
 * Wiki SessionStart Hook
 *
 * On session start:
 * 1. Check if docs/wiki/ exists with pages
 * 2. Rebuild index if missing
 * 3. Inject wiki context summary into conversation
 */

import { existsSync, readFileSync, readdirSync, mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

function readStdin(timeoutMs = 1000) {
  return new Promise((resolve) => {
    let data = '';
    const timer = setTimeout(() => resolve(data), timeoutMs);
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => { clearTimeout(timer); resolve(data); });
  });
}

function getWikiDir(root) {
  return join(root, process.env.WIKI_ROOT || join('docs', 'wiki'));
}

function listPages(wikiDir) {
  const reserved = new Set(['index.md', 'log.md', 'environment.md']);
  if (!existsSync(wikiDir)) return [];
  return readdirSync(wikiDir)
    .filter(f => f.endsWith('.md') && !reserved.has(f))
    .sort();
}

async function main() {
  const input = await readStdin();
  try {
    const data = JSON.parse(input);
    const root = data.cwd || process.cwd();
    const wikiDir = getWikiDir(root);

    if (!existsSync(wikiDir)) {
      console.log(JSON.stringify({ continue: true, suppressOutput: true }));
      return;
    }

    const pages = listPages(wikiDir);
    if (pages.length === 0) {
      console.log(JSON.stringify({ continue: true, suppressOutput: true }));
      return;
    }

    // Read or note missing index
    const indexPath = join(wikiDir, 'index.md');
    let indexContent = '';
    if (existsSync(indexPath)) {
      indexContent = readFileSync(indexPath, 'utf-8');
    }

    const summary = [
      `[LLM Wiki: ${pages.length} pages at docs/wiki/]`,
      '',
      'Use wiki_query to search, wiki_list to browse, wiki_read to view pages.',
      '',
      indexContent ? indexContent.split('\n').slice(0, 30).join('\n') : `Pages: ${pages.join(', ')}`,
    ].join('\n');

    console.log(JSON.stringify({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'SessionStart',
        additionalContext: summary,
      },
    }));
  } catch (error) {
    console.error('[dh-wiki-session-start] Error:', error.message);
    console.log(JSON.stringify({ continue: true, suppressOutput: true }));
  }
}

main();
