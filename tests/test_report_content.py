
from pathlib import Path

import pymupdf
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "sample_reports" / "monthly_orders_report.pdf"


@pytest.fixture(scope="module")
def report_text():
    """Extract all text from the generated PDF report."""
    assert REPORT_PATH.exists(), f"Report not found: {REPORT_PATH}"

    with pymupdf.open(REPORT_PATH) as pdf:
        return "\n".join(page.get_text() for page in pdf)


def test_report_title_and_period_exist(report_text):
    assert "Monthly Orders Report" in report_text
    assert "October 2026" in report_text


@pytest.mark.parametrize(
    "order_id",
    ["ORD-1001", "ORD-1002", "ORD-1003"],
)
def test_all_orders_are_present(report_text, order_id):
    assert order_id in report_text


def test_grand_total_is_correct(report_text):
    assert "$11,500.00" in report_text


def test_order_count_is_correct(report_text):
    assert "Total orders: 3" in report_text
