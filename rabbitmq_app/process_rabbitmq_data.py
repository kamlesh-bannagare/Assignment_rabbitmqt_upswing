import pika
import json

from Assignment_rabbitmqt_upswing.rabbitmq_app.database import collection

rabbitmq_host = 'localhost'
rabbitmq_queue = 'mqtt_queue'


def process_message(ch, method, properties, body):
  """
  This function processes incoming messages from the RabbitMQ queue.
  - Decodes the JSON message body.
  - Inserts the message data into the MongoDB collection using the provided collection object.
  - Prints a confirmation message indicating the received message.
  """
  message = json.loads(body)
  collection.insert_one(message)
  print(f" [x] Received message: {message}")


def start_mqtt_consumer():
  """
  This function establishes a connection to RabbitMQ, declares the queue,
  and starts consuming messages. It uses the process_message function as the callback
  for handling incoming messages.
  """
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
  channel = connection.channel()
  channel.queue_declare(queue=rabbitmq_queue)
  channel.basic_consume(queue=rabbitmq_queue, on_message_callback=process_message, auto_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
