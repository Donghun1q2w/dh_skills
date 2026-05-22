#!/usr/bin/env node

/**
 * Wiki UserPromptSubmit Hook
 *
 * Replaces SessionStart context injection. Fires on every user prompt,
 * so payload is kept compact: page count + top index lines only.
 */

import { existsSync, readFileSync, readdirSync } from 'fs';
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

    const indexPath = join(wikiDir, 'index.md');
    let topLines = '';
    if (existsSync(indexPath)) {
      const indexContent = readFileSync(indexPath, 'utf-8');
      topLines = indexContent.split('\n').slice(0, 5).join('\n');
    }

    const summary = [
      `[LLM Wiki: ${pages.length} pages at docs/wiki/]`,
      'Use dh_wiki_query/list/read to access wiki content.',
      topLines,
    ].filter(Boolean).join('\n');

    console.log(JSON.stringify({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'UserPromptSubmit',
        additionalContext: summary,
      },
    }));
  } catch (error) {
    console.error('[dh-wiki-user-prompt-submit] Error:', error.message);
    console.log(JSON.stringify({ continue: true, suppressOutput: true }));
  }
}

main();
