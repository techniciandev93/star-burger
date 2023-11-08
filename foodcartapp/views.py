from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order = request.data

    required_fields = ('address', 'phonenumber', 'lastname', 'firstname', 'products')
    checking_fields = [field for field in required_fields if field not in order]
    if checking_fields:
        content = {'error': f'Не переданы поля {checking_fields}'}
        return Response(content, status=status.HTTP_200_OK)

    if not isinstance(order['address'], str):
        content = {'error': 'Поле address должно быть строкой'}
        return Response(content, status=status.HTTP_200_OK)

    if not isinstance(order['phonenumber'], str):
        content = {'error': 'Поле phonenumber должно быть строкой'}
        return Response(content, status=status.HTTP_200_OK)

    if not isinstance(order['lastname'], str):
        content = {'error': 'Поле lastname должно быть строкой'}
        return Response(content, status=status.HTTP_200_OK)

    if not isinstance(order['firstname'], str):
        content = {'error': 'Поле firstname должно быть строкой'}
        return Response(content, status=status.HTTP_200_OK)

    if not isinstance(order['products'], list):
        content = {'error': 'В products должен быть список'}
        return Response(content, status=status.HTTP_200_OK)

    if not order['products']:
        content = {'error': 'Список products не может быть пустым'}
        return Response(content, status=status.HTTP_200_OK)


    instance_order = Order.objects.create(
        firstname=order['firstname'],
        lastname=order['lastname'],
        phone_number=order['phonenumber'],
        address=order['address']
    )

    products_ids = [product['product'] for product in order['products']]
    instance_products = {obj.id: obj for obj in Product.objects.filter(id__in=products_ids)}

    for product in order['products']:
        OrderItem.objects.create(
            product=instance_products[product['product']],
            order=instance_order,
            count=product['quantity']
        )
    return JsonResponse({'Create': True}, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })
