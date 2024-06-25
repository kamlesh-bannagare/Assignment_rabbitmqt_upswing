# Imports (assuming necessary libraries are installed)
import pytest
from fastapi.testclient import TestClient
from Assignment_rabbitmqt_upswing.rabbitmq_app.main import app # Adjust import path if needed
from pymongo.errors import PyMongoError  # Import for error handling tests
from datetime import datetime, timedelta
from unittest.mock import patch  # Mocking for external dependencies
from pymongo import MongoClient
import json
# Global variables (adjust as needed)
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'mqtt_queue'
MONGO_URI = 'mongodb://localhost:27017/'  # Assuming a connection URI


@pytest.fixture(scope="module")  # Fixture for MongoDB connection (shared across tests)
def mongo_fixture():
    client = MongoClient(MONGO_URI)
    db = client['mqtt_db']
    collection = db['mqtt_collection']

    # Clear collection before tests
    collection.delete_many({})

    yield collection

    # Clean collection after tests
    collection.delete_many({})
    client.close()


@pytest.fixture(scope="function")  # Fixture for TestClient (per test)
def client(mongo_fixture):
    with TestClient(app) as c:
        yield c


def test_get_status_count_valid_range(client, mongo_fixture):
    # Insert sample data
    now = datetime.utcnow()
    sample_data = [
        {"status": 0, "timestamp": now.timestamp()},
        {"status": 1, "timestamp": (now - timedelta(seconds=10)).timestamp()},
        {"status": 2, "timestamp": (now - timedelta(seconds=20)).timestamp()},
    ]
    mongo_fixture.insert_many(sample_data)

    # Define time range within inserted data
    start_time = (now - timedelta(seconds=15)).isoformat()
    end_time = now.isoformat()

    response = client.get(f"/status_count/?start_time={start_time}&end_time={end_time}")

    assert response.status_code == 200
    assert response.json() == {'0': 1, '1': 1}


def test_get_status_count_no_data(client, mongo_fixture):
    # No data inserted

    start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_time = (datetime.utcnow() + timedelta(days=2)).isoformat()

    response = client.get("/status_count/", json={"start_time": start_time, "end_time": end_time})

    assert response.status_code == 200
    assert response.json() == {}


def test_get_status_count_invalid_dates(client):
    # Invalid date formats

    invalid_data = [
        {"start_time": "invalid", "end_time": "invalid"},
        {"start_time": "2024-01-01", "end_time": "not-a-date"},
    ]

    for data in invalid_data:
        response = client.get(f"/status_count/?start_time={data["start_time"]}&end_time={data["end_time"]}")
        assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.usefixtures("mongo_fixture")  # Use shared MongoDB fixture
def test_process_message(mocker):
    # Mock RabbitMQ connection and channel
    connection_mock = mocker.Mock()
    channel_mock = mocker.Mock()
    connection_mock.channel.return_value = channel_mock

    # Mock message delivery
    message = {"status": 3}  # Sample message with status
    channel_mock.basic_consume.call_args = (mocker.ANY, mocker.ANY, mocker.ANY, json.dumps(message))

    # Call process_message with mocked connection
    # process_message(connection_mock, None, None, json.dumps(message))

    # Assert message is inserted into MongoDB
    mongo_fixture.insert_one.assert_called_once_with(message)


# @pytest.mark.usefixtures("mongo_fixture")  # Use shared MongoDB fixture
# def test_process_message_error(mocker, client):
#     # Mock insert_one to raise an error
#     mongo_fixture.insert_one.side_
