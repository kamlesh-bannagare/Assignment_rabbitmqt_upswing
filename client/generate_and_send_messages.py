import time
import random
import pika
import json

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_queue = 'mqtt_queue'

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue)

def emit_and_send_message():
    while True:
        status = random.randint(0, 6)
        message = json.dumps({"status": status, "timestamp": time.time()})
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
        print(f" [x] Sent {message}")
        time.sleep(1)

if __name__ == "__main__":
    emit_and_send_message()

