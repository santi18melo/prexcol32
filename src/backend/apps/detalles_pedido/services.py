from .tasks import generate_invoice_pdf_task

class InvoiceService:
    @staticmethod
    def trigger_pdf_generation(factura_id):
        generate_invoice_pdf_task.delay(factura_id)
