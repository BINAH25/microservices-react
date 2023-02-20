import os, pika, json

from dotenv import load_dotenv
load_dotenv()

params = pika.URLParameters(os.getenv("CLOUDAMQP_URL"))

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)