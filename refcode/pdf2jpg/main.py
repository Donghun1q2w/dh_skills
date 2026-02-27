"""Main entry point for PDF to JPG Converter.

Usage:
    python -m pdf2jpg
    python main.py
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path to allow imports when running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # Try absolute import first (when run as module or after path adjustment)
    from pdf2jpg.config import Settings, load_settings, setup_logging
    from pdf2jpg.converter import convert_batch, print_summary
except ImportError:
    # Fall back to relative import (when run as part of package)
    from .config import Settings, load_settings, setup_logging
    from .converter import convert_batch, print_summary

logger = logging.getLogger(__name__)


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, 1 for errors).
    """
    # Determine settings file location
    # Priority: 1) Command line arg, 2) Current directory, 3) Script directory
    if len(sys.argv) > 1:
        settings_path = Path(sys.argv[1])
    else:
        settings_path = Path("settings.json")
        if not settings_path.exists():
            # Try script directory
            script_dir = Path(__file__).parent.parent
            settings_path = script_dir / "settings.json"

    try:
        settings = load_settings(settings_path if settings_path.exists() else None)
    except Exception as e:
        print(f"Error loading settings: {e}", file=sys.stderr)
        return 1

    # Setup logging
    setup_logging(settings)

    logger.info("=" * 50)
    logger.info("PDF to JPG Converter v1.0.0")
    logger.info("=" * 50)
    logger.info(f"Input:  {settings.input_folder.resolve()}")
    logger.info(f"Output: {settings.output_folder.resolve()}")
    logger.info(f"DPI: {settings.dpi}, Quality: {settings.jpg_quality}")
    logger.info("=" * 50)

    # Run conversion
    batch_result = convert_batch(settings)

    # Print summary
    print_summary(batch_result)

    # Return exit code
    if batch_result.failed_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
