import webbrowser
from pathlib import Path
from html import escape

from PIL import Image, ImageChops, ImageEnhance


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"

BASELINE_PATH = REPORTS_DIR / "baseline.png"
CURRENT_PATH = REPORTS_DIR / "monthly_orders_report.png"
DIFF_PATH = REPORTS_DIR / "visual_diff.png"
HTML_PATH = REPORTS_DIR / "visual_comparison.html"


def create_diff(baseline_path: Path, current_path: Path, diff_path: Path):
    """Create an amplified pixel-difference image."""

    with Image.open(baseline_path) as baseline_image:
        baseline = baseline_image.convert("RGB")

    with Image.open(current_path) as current_image:
        current = current_image.convert("RGB")

    if baseline.size != current.size:
        raise ValueError(
            "Image dimensions differ: "
            f"Baseline={baseline.size}, Current={current.size}. "
            "Render both images with the same settings."
        )

    difference = ImageChops.difference(baseline, current)

    # Amplify small pixel differences so they are easier to see.
    difference = ImageEnhance.Contrast(difference).enhance(4)

    difference.save(diff_path)

    return baseline.size


def create_html():
    """Create a local HTML page showing baseline, current, and diff."""

    for image_path in (BASELINE_PATH, CURRENT_PATH):
        if not image_path.exists():
            raise FileNotFoundError(
                f"Required image not found: {image_path}\n"
                "Make sure the baseline is saved locally and the "
                "visual test has generated the current image."
            )

    width, height = create_diff(
        BASELINE_PATH,
        CURRENT_PATH,
        DIFF_PATH,
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PDF Visual Comparison</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 24px;
            background: #f4f6f8;
            color: #1f2937;
        }}
        h1 {{ margin-top: 0; }}
        .summary {{
            margin-bottom: 24px;
            color: #4b5563;
        }}
        .images {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
            align-items: start;
        }}
        .panel {{
            background: white;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            padding: 14px;
            overflow: hidden;
        }}
        .panel h2 {{
            font-size: 18px;
            margin: 0 0 12px;
        }}
        .panel img {{
            display: block;
            width: 100%;
            height: auto;
            border: 1px solid #e5e7eb;
        }}
        .note {{
            font-size: 13px;
            color: #6b7280;
            margin-top: 10px;
        }}
        @media (max-width: 900px) {{
            .images {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <h1>PDF Visual Comparison</h1>
    <p class="summary">
        Image dimensions: {width} × {height} pixels.
        The Diff is an amplified pixel-by-pixel difference,
        not the Applitools Visual AI result.
    </p>

    <main class="images">
        <section class="panel">
            <h2>Baseline</h2>
            <img src="baseline.png" alt="Baseline image">
            <p class="note">Original reference image</p>
        </section>

        <section class="panel">
            <h2>Current</h2>
            <img src="monthly_orders_report.png" alt="Current image">
            <p class="note">Latest rendered PDF page</p>
        </section>

        <section class="panel">
            <h2>Diff</h2>
            <img src="visual_diff.png" alt="Pixel difference image">
            <p class="note">Brighter areas indicate pixel differences</p>
        </section>
    </main>
</body>
</html>
"""

    HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"Comparison page created: {HTML_PATH}")
    webbrowser.open(HTML_PATH.resolve().as_uri())


if __name__ == "__main__":
    create_html()
