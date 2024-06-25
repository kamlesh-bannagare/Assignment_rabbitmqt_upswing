# Assignment_rabbitmqt_upswing

## Setup

### Prerequisites
- RabbitMQ
- MongoDB
- Python 3.8+

### Installation
1) install erlang
https://www.erlang.org/downloads

2) Install RabbitMQ and enable the MQTT plugin:
rabbitmq on windows
https://www.rabbitmq.com/docs/install-windows
   ```bash
   rabbitmq-plugins enable rabbitmq_mqtt
   rabbitmq-plugins enable rabbitmq_management

### clone project
use given command to clone project:
 - git clone https://github.com/kamlesh-bannagare/Assignment_rabbitmqt_upswing.git

### create Virtual environment and activate it
- py -m pip install --user virtualenv . Note: if not available
- py -m venv env
- .\env\Scripts\activate

### run project
- before running project install required packages in you env using requirements.txt file
- run client file which is generate_and_send_messages file
- run server using main.py file 