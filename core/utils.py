from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


def generate_invoice_pdf(billing):
    # Make sure the folder exists
    directory = 'media/invoices'
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f'invoice_{billing.id}.pdf')

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Invoice Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Invoice")

    # Billing Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Invoice ID: {billing.id}")
    c.drawString(50, height - 120, f"User: {billing.user.username}")
    c.drawString(50, height - 140, f"Amount: ${billing.amount}")
    c.drawString(50, height - 160, f"Billing Date: {billing.billing_date}")
    c.drawString(50, height - 180, f"Payment Status: {billing.payment_status}")

    c.showPage()
    c.save()

    return file_path
