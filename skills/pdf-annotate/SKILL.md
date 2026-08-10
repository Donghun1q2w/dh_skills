---
name: pdf-annotate
description: "Native PDF annotation guide using pypdf. Adds colored border-only Square boxes with Popup companions and always-visible Korean FreeText labels rendered via custom PIL-rasterized appearance streams, so Hangul displays correctly in any PDF viewer. Use when adding annotations or markup boxes to PDF files, highlighting regions in a PDF with colored rectangles and labels, implementing pypdf annotation code in Python, or when the user mentions 'PDF annotate', 'PDF 주석', 'PDF에 주석 추가', 'PDF 박스 표시', 'annotate PDF'. References the pdf_annotate package at refcode/pdf_annotate."
---

# Native PDF Annotation Guide

Follow this guide when attaching annotations to a PDF. Use the `refcode/pdf_annotate` package as the reference implementation.

Every annotated region produces three real PDF annotation objects: a colored border-only `/Square`, a native `/Popup` companion, and a `/FreeText` label whose appearance stream is a PIL-rasterized Hangul image. The page content stream is never re-encoded.

Invocation hint: accept an optional PDF path, annotation JSON path, output path, or font path when the user provides them.

## Reference Code Location

```
refcode/pdf_annotate/
├── __init__.py      # Public API re-exports, __version__, pypdf version guard
├── __main__.py      # python -m pdf_annotate entry point
├── config.py        # Calibration constants, PRESET_COLORS, DEFAULT_FONT
├── geometry.py      # Coordinate transforms and label placement (pure, no pypdf)
├── appearance.py    # PIL rasterization, image XObject, label /AP form
├── annotator.py     # BoxAnnotation, AnnotateResult, annotate_pdf() core
├── demo.py          # Synthetic 3-page PDF demo (--demo)
└── main.py          # load_annotations(), main() - CLI entry point
```

## Required Dependencies

| Package | Purpose |
|---------|---------|
| `pypdf` | All PDF reading, writing, and annotation objects. Tested with 6.6.2 - importing the package emits a `RuntimeWarning` on a different major version |
| `Pillow` | Rasterizes the Korean label glyphs only. Pages are never rasterized |
| Hangul TTF | Default `C:\Windows\Fonts\malgun.ttf` (absolute path). Override with the `PDF_ANNOTATE_FONT` environment variable or `--font` |

```bash
pip install pypdf Pillow
```

## Core Implementation Pattern

Build a list of `BoxAnnotation` values and hand it to `annotate_pdf()`.

```python
from pdf_annotate import BoxAnnotation, PRESET_COLORS, annotate_pdf

annotations = [
    BoxAnnotation(1, (0.10, 0.10, 0.45, 0.18), "인장강도 기준 미달", PRESET_COLORS["critical"]),
    BoxAnnotation(2, (0.20, 0.20, 0.60, 0.30), "치수 재확인 필요", "FFEB9C", subject="warning"),
]

result = annotate_pdf("input.pdf", annotations, "output.pdf")
print(result.drawn, result.page_count, result.skipped_oob)
```

### Coordinate system

`bbox` is `(left, top, right, bottom)` in **display-space fractional** coordinates: values in `0..1`, origin at the **top-left** of the page **as the viewer sees it**. This is the same convention OCR engines and vision models emit, so their output can be passed through unchanged.

Page `/Rotate` is handled internally. On a `/Rotate 90` page the width and height swap in display space, and the package converts each bbox into unrotated user space before writing `/Rect`.

### Deduplication

By default identical annotations collapse into one. Two entries with the same resulting `/Rect` (rounded to 0.01pt), the same color, and the same truncated label produce a single bundle. Pass `dedupe=False` to attach every entry:

```python
annotate_pdf("input.pdf", annotations, "output.pdf", dedupe=False)
```

## Key Rules

| Rule | Detail |
|------|--------|
| Imports | `from pypdf.annotations import FreeText, Popup, Rectangle` / `from pypdf.constants import AnnotationFlag` / low-level via `pypdf.generic`. `Rectangle` creates the PDF `/Square` subtype (name confusion warning) |
| pypdf version | Tested with pypdf 6.6.2. The `FreeText` constructor's color kwargs corrupt `/DA`, so overwrite `/DA` manually right after construction. Importing the package warns on a major version mismatch |
| FreeText border | Never pass `border_color` at all. A truthy value corrupts `/DA`; `None` injects `/BS` with `W=0` |
| Border-only box | `Rectangle(rect=..., interior_color=None)` writes no `/IC`, giving an unfilled outline |
| Popup linkage | Add the Square with `add_annotation()` **first**, then build `Popup(parent=square)`; after adding the popup set `square[/Popup] = popup.indirect_reference`. Reordering breaks the link |
| NoRotate label | FreeText `/F` = Print + NoRotate. Its `/Rect` transforms the chip's top-left **single point** only - do not min/max normalize two corners, or the label unfolds backwards at 90/270 |
| No /Matrix | The label `/AP` Form XObject must not carry a `/Matrix`. With NoRotate the `/BBox`-to-`/Rect` identity mapping is already correct at every rotation |
| Page bytes | `PdfWriter(clone_from=reader)` clones page bytes verbatim and only grows `/Annots`. Never re-encode |
| Private API | XObject registration uses `writer._add_object()` - no public replacement exists, so re-check it on any pypdf upgrade |
| Content stream | Appearance operators are ASCII, so encode them as `latin-1`. Hangul travels only through the PIL raster and the `TextStringObject` in `/Contents` |
| Korean font | Font load failure raises `OSError` immediately. Silent fallback is forbidden because it would silently mangle Hangul |
| Dedupe | Identical `(rect, color, label)` triples attach once by default; `annotate_pdf(..., dedupe=False)` disables it |
| Encoding | Read JSON with `read_text(encoding="utf-8")`; set `$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'` before running on Windows |

## Annotation Anatomy

One `BoxAnnotation` becomes three annotation objects sharing a `/NM` prefix of `pdf-annotate-p{page}-{seq}`:

| Object | `/NM` suffix | Role |
|--------|--------------|------|
| `/Square` | (none) | Colored 2pt outline around the region, `/Contents` carries the label text |
| `/Popup` | `-popup` | Acrobat-native comment popup, closed by default, linked both ways to the Square |
| `/FreeText` | `-label` | Always-visible label chip drawn from a custom `/AP /N` form XObject |

Consequences worth knowing:

- All three are ordinary annotations, so a viewer can select, move, or delete each one individually.
- Labels are capped at 50 characters. Longer text collapses whitespace and becomes 49 characters plus a horizontal ellipsis.
- Label placement tries above, below, then to the right of the box, then stacks downward up to 40 steps. Within that capacity chips never overlap. Beyond it placement is **best-effort**: the label is still attached and still clamped inside the page, but chips may overlap.
- On a rotated page Acrobat may draw the FreeText selection handles offset from the visible chip. The rendered content is correct; only the interactive handle box is misaligned.

## Preset Colors

| Key | Hex |
|-----|-----|
| `warning` | `FFEB9C` |
| `neutral` | `D9D9D9` |
| `critical` | `FFC7CE` |

These three values come from a report-review workflow, where they highlighted "needs attention", "not applicable", and "failed" rows respectively. The keys are only a convenience: any 6-digit hex string is accepted, with an optional leading `#` or a leading ARGB alpha byte.

## Annotation JSON Format

The CLI reads a UTF-8 JSON file holding a top-level list. `color` defaults to `FFC7CE` and `subject` defaults to empty.

```json
[
  {"page": 1, "bbox": [0.1, 0.2, 0.4, 0.3], "label": "치수 불일치", "color": "FFC7CE", "subject": "critical"},
  {"page": 2, "bbox": [0.5, 0.5, 0.8, 0.6], "label": "확인 필요", "color": "FFEB9C"}
]
```

Failure handling is split by scope. A file that cannot be read, is not valid JSON, or is not a top-level list aborts the run with exit code 1. An individual malformed record is reported on stderr as `skip: record[i]: reason` and the remaining records still process.

## Running the Reference Code

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
cd refcode

# Annotate a PDF
python -m pdf_annotate input.pdf annotations.json -o out.pdf

# Override the label font
python -m pdf_annotate input.pdf annotations.json -o out.pdf --font C:\Windows\Fonts\gulim.ttc

# Synthetic demo: writes demo_input.pdf and demo_annotated.pdf
python -m pdf_annotate --demo -o demo_output
```

The summary line reports both skip counters:

```
out=out.pdf drawn=7 pages=3 skipped_oob=0 skipped_invalid=0
```

`skipped_oob` counts annotations whose page number falls outside the document. `skipped_invalid` counts records rejected while parsing the JSON.

## When to Use This Skill

- When the user asks to add annotations, comments, or markup boxes to a PDF
- When highlighting or boxing regions of a PDF with colored rectangles and text labels
- When implementing pypdf annotation code in Python
- When Korean (or other non-Latin) label text must render correctly in PDF viewers
- When converting OCR or vision-model bounding boxes into reviewable PDF markup

## Additional Context

If `$ARGUMENTS` is provided:
- If a PDF path is given, target that file for annotation
- If a JSON path is given, load the annotation list from it
- If an output path is given, write the annotated PDF there
- If a font path is given, use it as the label font
