
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "sample_reports"


def generate_orders_report(output_path: Path) -> Path:
    """Generate a sample PDF report containing order data."""

    orders = [
        {"order_id": "ORD-1001", "product": "Laptop",
            "quantity": 2, "unit_price": 3500.00},
        {"order_id": "ORD-1002", "product": "Keyboard",
            "quantity": 5, "unit_price": 180.00},
        {"order_id": "ORD-1003", "product": "Monitor",
            "quantity": 3, "unit_price": 1200.00},
    ]

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#5D1739"),
            spaceAfter=8 * mm,
        )
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    story = []

    story.append(Paragraph("Monthly Orders Report", styles["ReportTitle"]))
    story.append(Paragraph("Reporting Period: October 2026", styles["Normal"]))
    story.append(Spacer(1, 8 * mm))

    table_data = [
        ["Order ID", "Product", "Quantity", "Unit Price", "Total"],
    ]

    grand_total = 0.0

    for order in orders:
        total = order["quantity"] * order["unit_price"]
        grand_total += total

        table_data.append(
            [
                order["order_id"],
                order["product"],
                str(order["quantity"]),
                f"${order['unit_price']:,.2f}",
                f"${total:,.2f}",
            ]
        )

    table_data.append(["", "", "", "Grand Total", f"${grand_total:,.2f}"])

    table = Table(
        table_data,
        colWidths=[28 * mm, 35 * mm, 22 * mm, 32 * mm, 32 * mm],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B7C9D6")),
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#D9EAF7")),
                ("FONTNAME", (3, -1), (-1, -1), "Helvetica-Bold"),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(f"Total orders: {len(orders)}", styles["Normal"]))

    document.build(story)

    return output_path


if __name__ == "__main__":
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = REPORTS_DIR / "monthly_orders_report.pdf"

    generate_orders_report(output_file)
    print(f"PDF report generated: {output_file}")
