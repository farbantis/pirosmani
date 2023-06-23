import redis
from django.core.mail import send_mail
from account.models import CustomerAdd
from cafe.models import OrderItems, Product
from pirosmani.celery import app
# from pirosmani.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
from pirosmani.utils.constants import EMAIL_NEW_USER_REG
from celery import shared_task


@shared_task
def transaction_email_notification(user):
    pass
    # email = user.email
    # subject = f'registration confirmation'
    # message = f"""
    #     Dear {email},
    #     you successfully placed the order
    #     the receipt is attached to this letter.
    #     your status is {user.customeradd.status}.
    # """
    # from_email = EMAIL_NEW_USER_REG
    # recipient_list = [email]
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def send_products_to_redis_with_frequency():
    pass
    # redis_product = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    # products = Product.objects.all()
    # for product in products:
    #     product_key = f"product:{product.id}"
    # #  send all products to redis
    #     redis_product.hmset(product_key, {
    #         'id': product.id,
    #         'name': product.name,
    #         'description': product.description,
    #         'price': str(product.price),
    #         'frequency': '0'  # Initialize frequency as 0
    #     })
    # #  calculate frequency of each item and write it to redis
    # order_items = OrderItems.objects.filter(order__is_completed=True)
    # for item in order_items:
    #     product_key = f"product:{item.product_id}"
    #     # redis_product[product_key]['frequency'] += item.quantity
    #     redis_product.hincrby(product_key, 'frequency', item.quantity)
    # #redis_product_sorted = redis_product.zrange("frequency_data", 0, -1, withscores=True)
    # redis_product.zadd("frequency_data", {product_key: int(redis_product.hget(product_key, 'frequency'))})
    # return redis_product

