---

## name: dh-wiki description: "LLM Wiki — persistent markdown knowledge base at docs/wiki/ with standalone MCP server (no OMC dependency)" triggers: \["wiki", "wiki this", "wiki add", "wiki lint", "wiki query"\]

# Wiki

Persistent, self-maintained markdown knowledge base for project and session knowledge. Inspired by Karpathy's LLM Wiki concept.

## Operations

### Ingest

Process knowledge into wiki pages. A single ingest can touch multiple pages.

```
dh_wiki_ingest({ title: "Auth Architecture", content: "...", tags: ["auth", "architecture"], category: "architecture" })
```

### Query

Search across all wiki pages by keywords and tags. Returns matching pages with snippets — YOU (the LLM) synthesize answers with citations from the results.

```
dh_wiki_query({ query: "authentication", tags: ["auth"], category: "architecture" })
```

### Lint

Run health checks on the wiki. Detects orphan pages, stale content, broken cross-references, oversized pages, and structural contradictions.

```
dh_wiki_lint()
```

### Quick Add

Add a single page quickly (simpler than ingest).

```
dh_wiki_add({ title: "Page Title", content: "...", tags: ["tag1"], category: "decision" })
```

### List / Read / Delete

```
dh_wiki_list()           # Show all pages (reads index.md)
dh_wiki_read({ page: "auth-architecture" })  # Read specific page
dh_wiki_delete({ page: "outdated-page" })    # Delete a page
```

### Log

View wiki operation history by reading `docs/wiki/log.md`.

## Categories

Pages are organized by category: `architecture`, `decision`, `pattern`, `debugging`, `environment`, `session-log`, `reference`, `convention`

## Storage

- Pages: `docs/wiki/*.md` (markdown with YAML frontmatter)
- Index: `docs/wiki/index.md` (auto-maintained catalog)
- Log: `docs/wiki/log.md` (append-only operation chronicle)

## Cross-References

Use `[[page-name]]` wiki-link syntax to create cross-references between pages.

## Auto-Capture

At session end, significant discoveries are automatically captured as session-log pages.

## Hard Constraints

- NO vector embeddings — query uses keyword + tag matching only
- Wiki pages are stored in `docs/wiki/` (git-tracked by default)
- Standalone MCP server — no OMC dependency required