/**
 * Wiki Types (pure JS — no TypeScript dependency)
 *
 * Constants and factory functions for the LLM Wiki knowledge layer.
 */

/** Current schema version for wiki pages. */
export const WIKI_SCHEMA_VERSION = 1;

/** Supported page categories. */
export const WIKI_CATEGORIES = [
  'architecture', 'decision', 'pattern', 'debugging',
  'environment', 'session-log', 'reference', 'convention',
];

/** Default wiki configuration. */
export const DEFAULT_WIKI_CONFIG = {
  autoCapture: true,
  staleDays: 30,
  maxPageSize: 10_240, // 10KB
};
