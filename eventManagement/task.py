# yourapp/tasks.py

from celery import shared_task
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from invoice.models import Invoice
from django.contrib.auth import get_user_model
from django.http import HttpResponse
User = get_user_model()

@shared_task
def generate_invoice_task(user_id, data):
    user = User.objects.get(id=user_id)

    html_string = render_to_string("./templates/invoice.html", data)
    pdf = HTML(string=html_string).write_pdf()

    invoice = Invoice.objects.create(user=user)

    invoice.file.save(
        f"invoice_{invoice.id}.pdf",
        ContentFile(pdf)
    )
    print('created ')

    return invoice.id