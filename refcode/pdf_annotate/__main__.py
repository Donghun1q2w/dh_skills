"""Allow running as python -m pdf_annotate."""

import sys

from .main import main

if __name__ == "__main__":
    sys.exit(main())
