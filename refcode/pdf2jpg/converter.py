"""PDF to JPG conversion module.

Core logic for converting PDF files to JPG images using PyMuPDF.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import pymupdf  # Use pymupdf instead of fitz to avoid namespace conflicts

from .config import Settings

logger = logging.getLogger(__name__)


@dataclass
class ConversionResult:
    """Result of a single PDF conversion."""

    pdf_path: Path
    status: Literal["success", "partial", "failed", "skipped"]
    pages_total: int = 0
    pages_converted: int = 0
    pages_failed: int = 0
    error_message: str | None = None
    output_files: list[Path] = field(default_factory=list)


@dataclass
class BatchResult:
    """Result of batch conversion."""

    total_files: int = 0
    success_count: int = 0
    partial_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    results: list[ConversionResult] = field(default_factory=list)

    def add(self, result: ConversionResult) -> None:
        """Add a conversion result to the batch."""
        self.results.append(result)
        self.total_files += 1
        match result.status:
            case "success":
                self.success_count += 1
            case "partial":
                self.partial_count += 1
            case "failed":
                self.failed_count += 1
            case "skipped":
                self.skipped_count += 1


def get_output_path(
    pdf_path: Path, page_num: int, output_folder: Path, fmt: str = "jpg"
) -> Path:
    """Generate output file path for a PDF page.

    Args:
        pdf_path: Source PDF file path.
        page_num: Page number (0-indexed).
        output_folder: Output directory.
        fmt: Output format extension.

    Returns:
        Path for the output image file.
    """
    stem = pdf_path.stem
    # Page number is 1-indexed in filename, zero-padded to 3 digits
    filename = f"{stem}_{page_num + 1:03d}.{fmt}"
    return output_folder / filename


def should_skip_pdf(pdf_path: Path, settings: Settings) -> bool:
    """Check if PDF should be skipped based on existing output files.

    Args:
        pdf_path: Source PDF file path.
        settings: Application settings.

    Returns:
        True if all expected output files exist and skip_if_exists is enabled.
    """
    if not settings.skip_if_exists or settings.overwrite:
        return False

    # We need to check if ANY output file exists
    # Since we don't know page count without opening, check for at least page 1
    first_page_path = get_output_path(pdf_path, 0, settings.output_folder, settings.format)
    if first_page_path.exists():
        logger.info(f"Skipping (output exists): {pdf_path.name}")
        return True

    return False


def convert_pdf(pdf_path: Path, settings: Settings) -> ConversionResult:
    """Convert a single PDF file to JPG images.

    Args:
        pdf_path: Path to the PDF file.
        settings: Application settings.

    Returns:
        ConversionResult with status and details.
    """
    result = ConversionResult(pdf_path=pdf_path, status="success")

    # Check if should skip
    if should_skip_pdf(pdf_path, settings):
        result.status = "skipped"
        return result

    try:
        doc = pymupdf.open(pdf_path)
    except pymupdf.FileDataError as e:
        logger.error(f"Corrupt PDF: {pdf_path.name} - {e}")
        result.status = "failed"
        result.error_message = f"Corrupt PDF: {e}"
        return result
    except Exception as e:
        logger.error(f"Failed to open: {pdf_path.name} - {e}")
        result.status = "failed"
        result.error_message = str(e)
        return result

    # Check for encryption
    if doc.is_encrypted:
        logger.warning(f"Encrypted PDF (skipping): {pdf_path.name}")
        doc.close()
        result.status = "failed"
        result.error_message = "Password protected"
        return result

    result.pages_total = len(doc)

    # Determine colorspace
    if settings.colorspace == "gray":
        cs = pymupdf.csGRAY
    else:
        cs = pymupdf.csRGB

    # Limit pages if configured
    max_pages = settings.max_pages_per_pdf if settings.max_pages_per_pdf > 0 else len(doc)
    pages_to_process = min(len(doc), max_pages)

    for page_num in range(pages_to_process):
        output_path = get_output_path(
            pdf_path, page_num, settings.output_folder, settings.format
        )

        # Check overwrite
        if output_path.exists() and not settings.overwrite:
            logger.debug(f"Skipping existing: {output_path.name}")
            result.pages_converted += 1
            result.output_files.append(output_path)
            continue

        try:
            page = doc.load_page(page_num)
            # Render with specified DPI (rotation is automatically handled by PyMuPDF)
            # alpha=False ensures white background for transparent content
            pix = page.get_pixmap(dpi=settings.dpi, colorspace=cs, alpha=False)

            # Apply crop if enabled
            if settings.crop.enabled:
                width = pix.width
                height = pix.height
                x0 = int(width * settings.crop.horizontal_start / 100)
                x1 = int(width * settings.crop.horizontal_end / 100)
                y0 = int(height * settings.crop.vertical_start / 100)
                y1 = int(height * settings.crop.vertical_end / 100)
                
                # Use PIL for cropping (more reliable)
                from PIL import Image
                import io
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                img_cropped = img.crop((x0, y0, x1, y1))
                if settings.format == "png":
                    img_cropped.save(str(output_path), "PNG")
                else:
                    img_cropped.save(str(output_path), "JPEG", quality=settings.jpg_quality)
                logger.debug(f"Cropped: ({x0},{y0}) to ({x1},{y1})")
                
                result.pages_converted += 1
                result.output_files.append(output_path)
                logger.debug(f"Converted: {output_path.name}")
                continue

            # Save with format-specific options
            if settings.format == "png":
                pix.save(str(output_path))
            else:
                pix.save(str(output_path), jpg_quality=settings.jpg_quality)

            result.pages_converted += 1
            result.output_files.append(output_path)
            logger.debug(f"Converted: {output_path.name}")

        except Exception as e:
            logger.error(f"Page {page_num + 1} failed in {pdf_path.name}: {e}")
            result.pages_failed += 1

    doc.close()

    # Determine final status
    if result.pages_failed == 0:
        result.status = "success"
        logger.info(
            f"✓ {pdf_path.name}: {result.pages_converted}/{result.pages_total} pages"
        )
    elif result.pages_converted > 0:
        result.status = "partial"
        logger.warning(
            f"⚠ {pdf_path.name}: {result.pages_converted}/{result.pages_total} pages "
            f"({result.pages_failed} failed)"
        )
    else:
        result.status = "failed"
        result.error_message = "All pages failed to render"
        logger.error(f"✗ {pdf_path.name}: All pages failed")

    return result


def convert_batch(settings: Settings) -> BatchResult:
    """Convert all PDFs in input folder.

    Args:
        settings: Application settings.

    Returns:
        BatchResult with summary and individual results.
    """
    batch_result = BatchResult()

    # Validate input folder
    if not settings.input_folder.exists():
        logger.error(f"Input folder not found: {settings.input_folder}")
        return batch_result

    # Create output folder if needed
    settings.output_folder.mkdir(parents=True, exist_ok=True)

    # Find all PDF files
    pdf_files = sorted(settings.input_folder.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"No PDF files found in: {settings.input_folder}")
        return batch_result

    logger.info(f"Found {len(pdf_files)} PDF file(s)")

    for pdf_path in pdf_files:
        result = convert_pdf(pdf_path, settings)
        batch_result.add(result)

        # Check fail_fast
        if settings.fail_fast and result.status == "failed":
            logger.error("fail_fast enabled. Stopping.")
            break

    return batch_result


def print_summary(batch_result: BatchResult) -> None:
    """Print conversion summary to console.

    Args:
        batch_result: Batch conversion result.
    """
    print("\n" + "=" * 50)
    print("CONVERSION SUMMARY")
    print("=" * 50)
    print(f"Total Files:    {batch_result.total_files}")
    print(f"  ✓ Success:    {batch_result.success_count}")
    print(f"  ⚠ Partial:    {batch_result.partial_count}")
    print(f"  ✗ Failed:     {batch_result.failed_count}")
    print(f"  ⊘ Skipped:    {batch_result.skipped_count}")
    print("=" * 50)

    # Show failed files
    failed = [r for r in batch_result.results if r.status == "failed"]
    if failed:
        print("\nFailed Files:")
        for r in failed:
            print(f"  - {r.pdf_path.name}: {r.error_message}")
