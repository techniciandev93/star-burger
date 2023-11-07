from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view

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
