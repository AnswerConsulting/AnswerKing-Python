from typing import Literal

from django.db.models import QuerySet
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from answerking_app.models.models import Order
from answerking_app.models.serializers import OrderSerializer
from answerking_app.utils.mixins.OrderItemMixins import (OrderItemRemoveMixin,
                                                         OrderItemUpdateMixin)


class OrderListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset: QuerySet = Order.objects.all()
    serializer_class: OrderSerializer = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request)


class OrderDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):

    queryset: QuerySet = Order.objects.all()
    serializer_class: OrderSerializer = OrderSerializer
    lookup_url_kwarg: Literal["order_id"] = "order_id"

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class OrderItemListView(
    OrderItemUpdateMixin,
    OrderItemRemoveMixin,
    generics.GenericAPIView,
):
    serializer_class: OrderSerializer = OrderSerializer
    lookup_url_kwarg: Literal["order_id"] = "order_id"

    def put(
        self, request: Request, order_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        return self.update(
            request, order_id=order_id, item_id=item_id, *args, **kwargs
        )

    def delete(
        self, request: Request, order_id: int, item_id: int, *args, **kwargs
    ) -> Response:
        return self.remove(request, order_id, item_id, *args, **kwargs)
