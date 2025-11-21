from django.shortcuts import render
import json

from django.views import View
from .models import Review
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

# Create your views here.
class ReviewsListView(View):
    def get(self, request):
        reviews = [r.to_dict() for r in Review.objects.all()]
        return JsonResponse({"reviews": reviews})
    
    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)

        product_id = data.get("product_id")
        user_id = data.get("user_id")
        rate = data.get("rate")
        comment = data.get("comment", "")

        if not product_id:
            return JsonResponse({"product_id": "Required."}, status=400)
        
        if not user_id:
            return JsonResponse({"user_id": "Required."}, status=400)

        if rate is None:
            return JsonResponse({"rate": "Required."}, status=400)
        if not (1 <= rate <= 5):
            return JsonResponse({"rate": "Must be between 1 and 5."}, status=400)

        review = Review.objects.create(
            product_id=product_id,
            user_id=user_id,
            rate=rate,
            comment=comment
        )

        return JsonResponse(review.to_dict(), status=201)
    

class ReviewDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        review = get_object_or_404(Review, pk=pk)

        return JsonResponse(review.to_dict())
    def put(self, request: HttpRequest, pk: int) -> JsonResponse:
        review = get_object_or_404(Review, pk=pk)
        data = json.loads(request.body)

        rate = data.get("rate")

        if rate is not None:
            if not (1 <= rate <= 5):
                return JsonResponse({"rate": "Must be between 1 and 5."}, status=400)
            review.rate = rate

        review.comment = data.get("comment", review.comment)

        review.save()

        return JsonResponse(review.to_dict())
    
    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        review = get_object_or_404(Review, pk=pk)
        review.delete()
        return JsonResponse({"message": "Review deleted successfully."}, status=204)