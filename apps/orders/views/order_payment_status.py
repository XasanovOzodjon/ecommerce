import json

from django.views import View
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from ..models import Order, OrderItem


class OrderPaymentStatusView(View):

    def patch(self, request: HttpRequest, pk: int) -> JsonResponse:
        
        orders_pay_status = []
        temp = Order.PaymentStatus
        for i in temp:
            orders_pay_status.append(str(i[0]))
            
        order = get_object_or_404(Order, pk=pk)
        data = json.loads(request.body)

        new_pay_status = data.get("payment_status")
        if new_pay_status not in orders_pay_status:
            return JsonResponse({"Error": "Invalid status"}, status=400)
        else:
            order.payment_status = new_pay_status
            order.save()
            return JsonResponse({'message': 'successfully'}, status=200)