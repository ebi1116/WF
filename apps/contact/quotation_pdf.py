"""Small dependency-free PDF renderer for saved quotations."""
import re
import unicodedata
from django.conf import settings


def _safe(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^\x20-\x7e]", "", text)


def _escape(value):
    return _safe(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _money(value):
    return f"Rs. {value:,.2f}"


def make_quotation_pdf(quote):
    """Render a clean one-page A4 quote using the PDF standard's base fonts."""
    commands = ["0.08 0.08 0.09 rg", "BT /F2 25 Tf 48 790 Td (QUOTATION) Tj ET",
                "1 0.38 0.18 rg", f"BT /F2 11 Tf 49 768 Td ({_escape(settings.QUOTATION_BUSINESS_NAME.upper())}) Tj ET",
                "0.2 0.2 0.22 rg", f"BT /F1 10 Tf 390 790 Td (Quote: {_escape(quote.number)}) Tj ET",
                f"BT /F1 10 Tf 390 772 Td (Date: {_escape(quote.issue_date.strftime('%d %b %Y'))}) Tj ET",
                f"BT /F1 10 Tf 390 754 Td (Valid until: {_escape(quote.valid_until.strftime('%d %b %Y') if quote.valid_until else 'Not specified')}) Tj ET",
                "0.85 0.85 0.87 RG 0.7 w 48 738 m 547 738 l S",
                "0.08 0.08 0.09 rg", "BT /F2 11 Tf 49 715 Td (PREPARED FOR) Tj ET",
                f"BT /F2 12 Tf 49 696 Td ({_escape(quote.customer_name)}) Tj ET"]
    seller_y = 751
    seller_details = (settings.QUOTATION_BUSINESS_EMAIL, settings.QUOTATION_BUSINESS_PHONE,
                      settings.QUOTATION_BUSINESS_ADDRESS,
                      f"GSTIN: {settings.QUOTATION_BUSINESS_GSTIN}" if settings.QUOTATION_BUSINESS_GSTIN else "")
    for value in seller_details:
        for line in _safe(value).splitlines():
            if line:
                commands.append(f"BT /F1 8 Tf 49 {seller_y} Td ({_escape(line[:80])}) Tj ET")
                seller_y -= 11
    y = 679
    for value in (quote.customer_company, quote.customer_email, quote.customer_phone, quote.customer_address):
        for line in _safe(value).splitlines():
            if line:
                commands.append(f"BT /F1 9 Tf 49 {y} Td ({_escape(line[:80])}) Tj ET")
                y -= 13
    table_y = min(y - 20, 635)
    commands += ["0.08 0.08 0.09 rg", f"0.96 0.96 0.97 rg 48 {table_y - 8} 499 25 re f",
                 f"BT /F2 9 Tf 56 {table_y} Td (DESCRIPTION) Tj ET",
                 f"BT /F2 9 Tf 342 {table_y} Td (QTY) Tj ET",
                 f"BT /F2 9 Tf 397 {table_y} Td (RATE) Tj ET",
                 f"BT /F2 9 Tf 490 {table_y} Td (AMOUNT) Tj ET"]
    row_y = table_y - 28
    for item in quote.items.all():
        label = _safe(item.description)
        commands.append(f"BT /F1 9 Tf 56 {row_y} Td ({_escape(label[:48])}) Tj ET")
        commands.append(f"BT /F1 9 Tf 342 {row_y} Td ({item.quantity:,.2f}) Tj ET")
        commands.append(f"BT /F1 9 Tf 397 {row_y} Td ({_money(item.unit_price)}) Tj ET")
        commands.append(f"BT /F1 9 Tf 490 {row_y} Td ({_money(item.amount)}) Tj ET")
        commands.append(f"0.9 0.9 0.91 RG 0.4 w 48 {row_y - 9} m 547 {row_y - 9} l S")
        row_y -= 26
    # Totals are anchored to the lower right; the 12 item form cap keeps this on one page.
    y_total = max(row_y - 12, 205)
    commands += [f"BT /F1 10 Tf 380 {y_total} Td (Subtotal) Tj ET",
                 f"BT /F1 10 Tf 480 {y_total} Td ({_money(quote.subtotal)}) Tj ET"]
    y_total -= 18
    if quote.discount:
        commands += [f"BT /F1 10 Tf 380 {y_total} Td (Discount) Tj ET",
                     f"BT /F1 10 Tf 480 {y_total} Td (- {_money(quote.discount)}) Tj ET"]
        y_total -= 18
    if quote.tax_percent:
        commands += [f"BT /F1 10 Tf 380 {y_total} Td (Tax {quote.tax_percent}%) Tj ET",
                     f"BT /F1 10 Tf 480 {y_total} Td ({_money(quote.tax_amount)}) Tj ET"]
        y_total -= 22
    commands += ["1 0.38 0.18 rg", f"BT /F2 13 Tf 380 {y_total} Td (TOTAL) Tj ET",
                 f"BT /F2 13 Tf 470 {y_total} Td ({_money(quote.total)}) Tj ET"]
    if quote.notes:
        notes_y = max(y_total - 42, 75)
        commands += ["0.08 0.08 0.09 rg", f"BT /F2 10 Tf 49 {notes_y} Td (NOTES AND TERMS) Tj ET"]
        for index, line in enumerate(_safe(quote.notes).splitlines()[:3]):
            commands.append(f"BT /F1 9 Tf 49 {notes_y - 16 - index * 13} Td ({_escape(line[:100])}) Tj ET")
    commands += ["0.65 0.65 0.67 rg", "BT /F1 8 Tf 49 35 Td (Thank you for considering WebFixer.) Tj ET"]
    content = "\n".join(commands).encode("ascii")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode("ascii") + obj + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode("ascii"))
    return bytes(output)
