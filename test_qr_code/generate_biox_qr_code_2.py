"""
Generate a QR code for the BioX Systems website with
additional white space around the QR code.
"""

from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H


QR_BACKGROUND_COLOR = "white"
QR_FOREGROUND_COLOR = "black"

CANVAS_SIZE = 450
QR_SIZE = 340


def generate_qr_code(url: str, output_file: Path) -> None:
    """
    Generate a centered QR code on a white square canvas.

    Args:
        url: URL to encode.
        output_file: Destination PNG file.
    """
    qr_code = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr_code.add_data(url)
    qr_code.make(fit=True)

    qr_image = qr_code.make_image(
        fill_color=QR_FOREGROUND_COLOR,
        back_color=QR_BACKGROUND_COLOR,
    ).convert("RGB")

    qr_image = qr_image.resize(
        (QR_SIZE, QR_SIZE),
        Image.Resampling.NEAREST,
    )

    canvas = Image.new(
        "RGB",
        (CANVAS_SIZE, CANVAS_SIZE),
        QR_BACKGROUND_COLOR,
    )

    offset = (CANVAS_SIZE - QR_SIZE) // 2
    canvas.paste(qr_image, (offset, offset))

    canvas.save(output_file)


def main() -> None:
    """Create the BioX Systems QR code image."""
    website_url = "https://www.bioxsystems.com/"
    output_file = Path("biox_systems_qr_code.png")

    generate_qr_code(website_url, output_file)

    print(f"QR code saved to: {output_file.resolve()}")


if __name__ == "__main__":
    main()

