---
name: pdf2img
description: PDF to image conversion guide. Use when converting PDF files to JPG/image files, implementing PDF-to-image conversion code in Python, or when the user asks to turn PDFs into images. References the pdf2jpg package at refcode/pdf2jpg.
argument-hint: "[optional: PDF path, output path, or specific settings like DPI/quality]"
---

# PDF to Image Conversion Guide

Follow this guide when converting PDFs to images (JPG). Use the `refcode/pdf2jpg` package as the reference implementation.

## Reference Code Location

```
refcode/pdf2jpg/
├── __init__.py      # Package init
├── __main__.py      # python -m pdf2jpg entry point
├── config.py        # Settings, CropSettings dataclass, load_settings(), setup_logging()
├── converter.py     # convert_pdf(), convert_batch(), ConversionResult, BatchResult
└── main.py          # main() function - CLI entry point
```

## Required Dependencies

| Package | Purpose |
|---------|---------|
| `pymupdf` | PDF rendering (PyMuPDF). Use `import pymupdf` (NOT `fitz`) |
| `Pillow` | Required only when using crop functionality |

```bash
pip install pymupdf Pillow
```

## Core Implementation Pattern

Always follow this pattern when writing PDF-to-image conversion code.

### Single PDF Conversion

```python
import pymupdf  # NOT import fitz

def convert_pdf_to_images(pdf_path, output_folder, dpi=300, jpg_quality=100, colorspace="rgb"):
    doc = pymupdf.open(pdf_path)

    if doc.is_encrypted:
        raise ValueError(f"Encrypted PDF: {pdf_path}")

    cs = pymupdf.csGRAY if colorspace == "gray" else pymupdf.csRGB

    output_files = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi, colorspace=cs, alpha=False)

        stem = Path(pdf_path).stem
        output_path = Path(output_folder) / f"{stem}_{page_num + 1:03d}.jpg"
        pix.save(str(output_path), jpg_quality=jpg_quality)
        output_files.append(output_path)

    doc.close()
    return output_files
```

### Key Rules

| Rule | Detail |
|------|--------|
| Import | Use `import pymupdf`. Never use `import fitz` (namespace conflict) |
| Alpha | `alpha=False` is required - ensures white background for transparent content |
| Filename | Format: `{stem}_{page_num+1:03d}.{format}` (1-indexed, 3-digit zero-padded) |
| Save | JPG: `pix.save(str(output_path), jpg_quality=...)` / PNG: `pix.save(str(output_path))` - Path objects must be converted with str() |
| Encryption | Always check `doc.is_encrypted` before conversion |
| Close | Always call `doc.close()` when done |

### Crop Support (Optional)

Use PIL when cropping is needed:

```python
from PIL import Image
import io

pix = page.get_pixmap(dpi=dpi, colorspace=cs, alpha=False)

# Percentage-based crop (0-100)
x0 = int(pix.width * h_start / 100)
x1 = int(pix.width * h_end / 100)
y0 = int(pix.height * v_start / 100)
y1 = int(pix.height * v_end / 100)

img_data = pix.tobytes("ppm")
img = Image.open(io.BytesIO(img_data))
img_cropped = img.crop((x0, y0, x1, y1))
img_cropped.save(str(output_path), "JPEG", quality=jpg_quality)
```

## Configuration (settings.json)

Settings can be managed via `settings.json`:

```json
{
    "input_folder": "./input",
    "output_folder": "./output",
    "dpi": 300,
    "format": "jpg",  // "jpg" or "png"
    "jpg_quality": 90,
    "colorspace": "rgb",
    "overwrite": false,
    "skip_if_exists": true,
    "max_pages_per_pdf": 0,
    "fail_fast": false,
    "log_file": null,
    "crop": {
        "enabled": false,
        "horizontal": { "start": 0, "end": 100 },
        "vertical": { "start": 0, "end": 100 }
    }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `dpi` | 300 | Resolution (72-1200 recommended) |
| `jpg_quality` | 90 | JPG quality (1-100) |
| `colorspace` | "rgb" | `"rgb"` or `"gray"` |
| `overwrite` | false | Overwrite existing output files |
| `skip_if_exists` | true | Skip conversion if output file already exists |
| `max_pages_per_pdf` | 0 | Max pages per PDF (0 = unlimited) |
| `fail_fast` | false | Stop immediately on failure |

## Running the Reference Code

How to run the reference code directly:

```bash
# Run as module
python -m pdf2jpg

# Specify settings.json path
python -m pdf2jpg /path/to/settings.json
```

## When to Use This Skill

- When the user asks to convert PDF files to images
- When implementing PDF-to-image conversion code in Python
- When writing batch PDF conversion scripts
- When extracting cropped page regions from PDFs as images

## Additional Context

If `$ARGUMENTS` is provided:
- If a PDF path is given, target that file for conversion
- If an output path is given, use it as the output_folder
- If DPI/quality settings are specified, apply those values
