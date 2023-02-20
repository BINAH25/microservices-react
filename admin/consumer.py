import pika, json, os, django
from django.conf import settings

# necessary because this is outside of the django app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from products.models import Product

params = pika.URLParameters(settings.CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='admin')

def callback(channel, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased.')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()