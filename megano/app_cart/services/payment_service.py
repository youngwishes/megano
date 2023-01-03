from interfaces.services import Service


class PaymentService(Service):
    def pay_for_order(self, cart):
        return True

    def get_order_status(self, order):
        return True
