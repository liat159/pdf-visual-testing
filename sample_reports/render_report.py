
from pathlib import Path

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "sample_reports" / "monthly_orders_report.pdf"
IMAGE_PATH = PROJECT_ROOT / "sample_reports" / "monthly_orders_report.png"


def render_pdf_page_to_image(
    pdf_path: Path,
    image_path: Path,
    page_number: int = 0,
    scale: float = 2.0,
) -> Path:
    """Render a PDF page to a PNG image for visual testing."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF report not found: {pdf_path}")

    with pymupdf.open(pdf_path) as pdf:
        if page_number < 0 or page_number >= len(pdf):
            raise ValueError(
                f"Page number {page_number} is invalid. "
                f"PDF contains {len(pdf)} page(s)."
            )

        page = pdf[page_number]
        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(scale, scale),
            alpha=False,
        )

        image_path.parent.mkdir(parents=True, exist_ok=True)
        pixmap.save(str(image_path))

    return image_path


if __name__ == "__main__":
    rendered_image = render_pdf_page_to_image(PDF_PATH, IMAGE_PATH)
    print(f"Rendered image: {rendered_image}")
