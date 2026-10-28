

import os
from pathlib import Path

import pytest
from applitools.images import Eyes, BatchInfo

from sample_reports.generate_report import generate_orders_report
from sample_reports.render_report import render_pdf_page_to_image


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = (
    PROJECT_ROOT
    / "sample_reports"
    / "monthly_orders_report.pdf"
)

IMAGE_PATH = (
    PROJECT_ROOT
    / "reports"
    / "monthly_orders_report.png"
)


@pytest.fixture
def eyes():
    api_key = os.getenv("APPLITOOLS_API_KEY")

    if not api_key:
        pytest.fail(
            "APPLITOOLS_API_KEY environment variable is not configured"
        )

    eyes = Eyes()
    eyes.api_key = api_key
    eyes.configure.batch = BatchInfo("PDF Visual Testing")

    yield eyes

    eyes.abort()


def test_monthly_report_visual(eyes):
    # Step 1: Generate a fresh PDF
    generate_orders_report(PDF_PATH)

    # Step 2: Render the PDF into an image
    IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    image_path = render_pdf_page_to_image(
        PDF_PATH,
        IMAGE_PATH,
    )

    # Step 3: Compare the image with the Applitools baseline
    eyes.open(
        "PDF Visual Testing",
        "Monthly Orders Report",
    )

    eyes.check_image(str(image_path))

    # Step 4: Fail pytest if visual differences are found
    eyes.close(True)
