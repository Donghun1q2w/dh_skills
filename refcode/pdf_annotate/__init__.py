"""Native PDF box-annotation package (pypdf Square + Popup + Korean FreeText labels)."""

import warnings

import pypdf

if not pypdf.__version__.startswith("6."):
    warnings.warn(
        f"pdf_annotate was validated against pypdf 6.6.2 (found {pypdf.__version__}); "
        "re-check FreeText /DA handling and writer._add_object before trusting output.",
        RuntimeWarning,
    )

from .annotator import AnnotateResult, BoxAnnotation, annotate_pdf
from .config import PRESET_COLORS
from .main import load_annotations

__version__ = "1.0.0"
__all__ = ["AnnotateResult", "BoxAnnotation", "annotate_pdf", "PRESET_COLORS", "load_annotations"]
