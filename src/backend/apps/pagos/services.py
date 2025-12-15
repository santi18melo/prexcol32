from .models import Pago, Transaccion

class PaymentService:
    @staticmethod
    def create_payment(user, validated_data):
        # Additional business logic for payment creation if needed
        return Pago.objects.create(usuario=user, **validated_data)

    @staticmethod
    def register_transaction(pago, data):
        """
        Registers a transaction for a payment.
        """
        return Transaccion.objects.create(pago=pago, **data)

    @staticmethod
    def get_payment_status(pago):
        return {
            "pago_id": pago.id,
            "estado": pago.estado.nombre,
            "descripcion": pago.estado.descripcion
        }
