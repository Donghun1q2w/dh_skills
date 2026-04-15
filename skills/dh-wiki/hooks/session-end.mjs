#!/usr/bin/env node

/**
 * Wiki SessionEnd Hook
 *
 * Auto-capture session metadata as a session-log wiki page.
 * Only runs if docs/wiki/ already exists (doesn't create wiki dir on first session).
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
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

function loadConfig(root) {
  const defaults = { autoCapture: true, staleDays: 30, maxPageSize: 10240 };
  try {
    const configPath = join(root, 'wiki.config.json');
    if (existsSync(configPath)) {
      const raw = JSON.parse(readFileSync(configPath, 'utf-8'));
      return { ...defaults, ...raw };
    }
  } catch { /* use defaults */ }
  return defaults;
}

async function main() {
  const input = await readStdin();
  try {
    const data = JSON.parse(input);
    const root = data.cwd || process.cwd();
    const config = loadConfig(root);

    if (!config.autoCapture) {
      console.log(JSON.stringify({ continue: true, suppressOutput: true }));
      return;
    }

    const wikiDir = getWikiDir(root);
    if (!existsSync(wikiDir)) {
      console.log(JSON.stringify({ continue: true, suppressOutput: true }));
      return;
    }

    const sessionId = data.session_id || `session-${Date.now()}`;
    const now = new Date().toISOString();
    const dateSlug = now.split('T')[0];
    const filename = `session-log-${dateSlug}-${sessionId.slice(-8)}.md`;
    const filePath = join(wikiDir, filename);

    const pageContent = [
      '---',
      `title: "Session Log ${dateSlug}"`,
      `tags: ["session-log", "auto-captured"]`,
      `created: ${now}`,
      `updated: ${now}`,
      `sources: ["${sessionId}"]`,
      `links: []`,
      `category: session-log`,
      `confidence: medium`,
      `schemaVersion: 1`,
      '---',
      '',
      `# Session Log ${dateSlug}`,
      '',
      'Auto-captured session metadata.',
      `Session ID: ${sessionId}`,
      '',
      'Review and promote significant findings to curated wiki pages via `wiki_ingest`.',
      '',
    ].join('\n');

    writeFileSync(filePath, pageContent, 'utf-8');

    // Append to log
    const logPath = join(wikiDir, 'log.md');
    const logEntry = `## [${now}] ingest\n- **Pages:** ${filename}\n- **Summary:** Auto-captured session log for ${sessionId}\n\n`;
    let logContent = '';
    if (existsSync(logPath)) {
      logContent = readFileSync(logPath, 'utf-8');
    } else {
      logContent = '# Wiki Log\n\n';
    }
    writeFileSync(logPath, logContent + logEntry, 'utf-8');

    console.log(JSON.stringify({ continue: true, suppressOutput: true }));
  } catch (error) {
    console.error('[dh-wiki-session-end] Error:', error.message);
    console.log(JSON.stringify({ continue: true, suppressOutput: true }));
  }
}

main();
