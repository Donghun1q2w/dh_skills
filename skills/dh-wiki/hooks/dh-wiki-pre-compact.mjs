#!/usr/bin/env node

/**
 * Wiki PreCompact Hook
 *
 * Before context compaction, inject wiki summary so the LLM
 * retains awareness of wiki state across compaction boundaries.
 */

import { existsSync, readdirSync } from 'fs';
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

    const reserved = new Set(['index.md', 'log.md', 'environment.md']);
    const pages = readdirSync(wikiDir)
      .filter(f => f.endsWith('.md') && !reserved.has(f));

    if (pages.length === 0) {
      console.log(JSON.stringify({ continue: true, suppressOutput: true }));
      return;
    }

    console.log(JSON.stringify({
      continue: true,
      hookSpecificOutput: {
        hookEventName: 'PreCompact',
        additionalContext: `[Wiki: ${pages.length} pages at docs/wiki/ — use dh_wiki_query to search, dh_wiki_list to browse]`,
      },
    }));
  } catch (error) {
    console.error('[dh-wiki-pre-compact] Error:', error.message);
    console.log(JSON.stringify({ continue: true, suppressOutput: true }));
  }
}

main();
