from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


class AddtoCart(APIView):
    
    def post(self, request):
        data = OrderItemSerializer(request.data).data
        user = User.objects.get(email=data['email'])
        if data['type'].lower() == "recipe":
            item = get_object_or_404(Recipe, id=data['recipe_id'])

            orderitem, created =  OrderItem.objects.get_or_create(
                type=data['type'],
                recipe = item,
                user = user
            )

            order_qs = Order.objects.filter(user=user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(recipe__id=item.id).exists():
                    orderitem.quantity += 1
                    orderitem.save()
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item updated"
                    })
                else:
                    order.items.add(orderitem)
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item Added"
                    })
            else:
                order = Order.objects.create(user=user)
                order.save()
                order.items.add(orderitem)
                return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item Added"
                    })
        else:
            item = get_object_or_404(Glocery, id=data['glocery_id'])

            orderitem, created =  OrderItem.objects.get_or_create(
                type=data['type'],
                glocery = item,
                user = user
            )

            order_qs = Order.objects.filter(user=user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(glocery__id=item.id).exists():
                    orderitem.quantity += 1
                    orderitem.save()
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item updated"
                    })
                else:
                    order.items.add(orderitem)
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item Added"
                    })
            else:
                order = Order.objects.create(user=user)
                order.save()
                order.items.add(orderitem)
                return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item Added"
                    })

class RemoveFromCart(APIView):
    def post(self, request, id):
        item = OrderItem.objects.get(id=id)
        if int(item.quantity) > 1:
            item.quantity -= 1
            item.save()
            return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item Updated"
                    })

        else:
            item.delete()
            return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item removed"
                    })

class RemoveItemDirect(APIView):
    
    def post(self, request, email):
        item = OrderItem.objects.get(email=email)

        item.delete()

        return Response({
                        "status": status.HTTP_200_OK,
                        "message":"Item Removed"
                    })  

class GetCartItems(APIView):
    permission_classes=()
    def get(self, request, email):
        user = User.objects.get(email=email)

        order = Order.objects.filter(user=user, ordered=False)

        if order.exists():
            order = order.first()
            items = order.items.all()
            items = OrderItemSerializerList(items, many=True)

            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":items.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":[]
                },
                status=status.HTTP_200_OK
            )


