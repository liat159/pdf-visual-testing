
import os

import pytest
from PIL import Image, ImageDraw
from applitools.images import Eyes, BatchInfo


@pytest.fixture
def eyes():
    eyes = Eyes()
    eyes.api_key = os.environ["APPLITOOLS_API_KEY"]
    eyes.configure.batch = BatchInfo("PDF Visual Testing - Learning")

    yield eyes

    eyes.abort()


def test_visual_smoke(eyes):
    image = Image.new("RGB", (800, 400), "white")
    draw = ImageDraw.Draw(image)

    draw.text((40, 40), "Monthly Report", fill="black")
    draw.text((40, 100), "Total Orders: 125", fill="black")
    draw.text((40, 160), "Status: Complete", fill="black")

    eyes.open(
        "PDF Visual Testing",
        "Smoke Test - Report Image",
    )

    eyes.check_image(image)
    eyes.close(False)
