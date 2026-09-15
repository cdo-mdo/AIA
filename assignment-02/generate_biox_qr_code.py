"""
Generate a QR code for the BioX Systems website.

The generated QR code uses:
- Black modules
- White background
- Standard quiet-zone border
- High error-correction level
"""

from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H


def generate_qr_code(url: str, output_file: Path) -> None:
    """
    Generate a QR code for the specified URL and save it as an image.

    Args:
        url: The URL that will be encoded in the QR code.
        output_file: Path where the generated PNG image will be saved.
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
        fill_color="black",
        back_color="white",
    )

    qr_image.save(output_file)


def main() -> None:
    """Generate the BioX Systems website QR code."""
    website_url = "https://www.bioxsystems.com/"
    output_file = Path("biox_systems_qr_code.png")

    generate_qr_code(website_url, output_file)

    print(f"QR code created successfully: {output_file.resolve()}")


if __name__ == "__main__":
    main()

