import os

from django.conf import settings

import pika

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

params = pika.URLParameters(settings.CLOUDAMQP_URL)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='admin')

def callback(channel, method, properties, body):
    print('Received in admin')
    print(body)

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()