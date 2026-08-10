"""Self-contained demo: synthetic 3-page PDF + preset-colored Korean annotations."""

from pathlib import Path

from pypdf import PdfWriter
from pypdf.generic import NameObject, NumberObject

from .annotator import AnnotateResult, BoxAnnotation, annotate_pdf
from .config import DEFAULT_FONT, PRESET_COLORS

A4_W, A4_H = 595.0, 842.0


def make_demo_pdf(path) -> Path:
    """Three blank A4 pages; page 2 is /Rotate 90 and page 3 is /Rotate 180."""
    path = Path(path)
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=A4_W, height=A4_H)
    writer.pages[1][NameObject("/Rotate")] = NumberObject(90)
    writer.pages[2][NameObject("/Rotate")] = NumberObject(180)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        writer.write(fh)
    return path


def demo_annotations() -> list[BoxAnnotation]:
    return [
        BoxAnnotation(1, (0.10, 0.10, 0.45, 0.18), "인장강도 기준 미달", PRESET_COLORS["critical"], "critical"),
        BoxAnnotation(1, (0.10, 0.30, 0.45, 0.38), "치수 재확인 필요", PRESET_COLORS["warning"], "warning"),
        # overlapping pair - demonstrates label collision avoidance
        BoxAnnotation(1, (0.55, 0.30, 0.90, 0.38), "해당 없음 — 시험 생략", PRESET_COLORS["neutral"], "neutral"),
        BoxAnnotation(1, (0.55, 0.31, 0.90, 0.39), "중복 영역 두 번째 항목", PRESET_COLORS["warning"], "warning"),
        # past 50 characters - demonstrates truncation
        BoxAnnotation(1, (0.10, 0.55, 0.90, 0.62),
                      "이 라벨은 오십 글자를 초과하도록 일부러 아주 길게 작성한 한글 문장으로서 말줄임 처리 동작을 보여준다",
                      PRESET_COLORS["critical"], "critical"),
        BoxAnnotation(2, (0.20, 0.20, 0.60, 0.30), "회전 페이지(90도) 주석", PRESET_COLORS["warning"], "warning"),
        BoxAnnotation(3, (0.20, 0.20, 0.60, 0.30), "회전 페이지(180도) 주석", PRESET_COLORS["critical"], "critical"),
    ]


def run_demo(out_dir, font_path=DEFAULT_FONT) -> AnnotateResult:
    out_dir = Path(out_dir)
    src = make_demo_pdf(out_dir / "demo_input.pdf")
    return annotate_pdf(src, demo_annotations(), out_dir / "demo_annotated.pdf", font_path=font_path)
