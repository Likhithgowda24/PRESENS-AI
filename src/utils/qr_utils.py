"""
QR Code Generator Utility for PRESENS AI
Uses segno if installed, with PIL/URL fallback if not installed.
"""

import io

try:
    import segno
    SEGNO_AVAILABLE = True
except ImportError:
    SEGNO_AVAILABLE = False

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def generate_qr_code_image(text_or_url: str) -> bytes:
    """
    Generate QR code PNG image bytes using segno.
    Falls back to a clean mock QR pattern if segno is not installed.
    """
    if SEGNO_AVAILABLE:
        qr = segno.make(text_or_url, error="h")
        buf = io.BytesIO()
        qr.save(buf, kind="png", scale=10, border=1)
        buf.seek(0)
        return buf.getvalue()

    # Fallback placeholder image
    if PIL_AVAILABLE:
        img = Image.new("RGB", (250, 250), color="white")
        draw = ImageDraw.Draw(img)
        # Draw mock QR corner squares
        for x, y in [(20, 20), (170, 20), (20, 170)]:
            draw.rectangle([x, y, x + 60, y + 60], outline="black", width=6)
            draw.rectangle([x + 15, y + 15, x + 45, y + 45], fill="black")
        draw.text((70, 115), "PRESENS QR", fill="black")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf.getvalue()

    return b""
