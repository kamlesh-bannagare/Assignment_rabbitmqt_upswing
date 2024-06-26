import time
import random
import pika
import json

rabbitmq_host = 'localhost'
rabbitmq_queue = 'mqtt_queue'

# Establish connection to RabbitMQ
try:
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
  channel = connection.channel()
except pika.exceptions.ConnectionClosed:
  # Handle connection errors gracefully (e.g., retry or log error)
  print("Failed to connect to RabbitMQ. Exiting.")
  exit(1)

# Declare the queue (ideally in a separate function for clarity)
def declare_rabbitmq_queue():
  channel.queue_declare(queue=rabbitmq_queue)

declare_rabbitmq_queue()  # Call the function to declare the queue

def emit_and_send_message():
  """sending status updates every second."""
  while True:
    status = random.randint(0, 6)  # Generate random status between 0 and 6
    message = json.dumps({"status": status, "timestamp": time.time()})
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
    print(f" [x] Sent message: {message}")
    time.sleep(1)

if __name__ == "__main__":
  emit_and_send_message()


