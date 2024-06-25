import pika
import json
from Assignment_rabbitmqt_upswing.rabbitmq_app.database import collection

rabbitmq_host = 'localhost'
rabbitmq_queue = 'mqtt_queue'

def process_message(ch, method, properties, body):
    message = json.loads(body)
    collection.insert_one(message)
    print(f" [x] Received {message}")

def start_mqtt_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=process_message, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
