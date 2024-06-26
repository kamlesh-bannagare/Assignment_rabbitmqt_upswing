import pytest
from fastapi.testclient import TestClient
from Assignment_rabbitmqt_upswing.rabbitmq_app.main import app  # Adjust import path if needed
from pymongo.errors import PyMongoError  # Import for error handling tests
from datetime import datetime, timedelta
from unittest.mock import patch  # Mocking for external dependencies
from pymongo import MongoClient
import json

RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'mqtt_queue'
MONGO_URI = 'mongodb://localhost:27017/'  # Assuming a connection URI

@pytest.fixture(scope="module")  # Fixture for MongoDB connection (shared across tests)
def mongo_fixture():
    """
    Setup a MongoDB connection and clear the collection before tests.
    This fixture is shared across all tests within the module.
    """
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
    """
    Setup a TestClient for the FastAPI app.
    This fixture is created for each test function.
    """
    with TestClient(app) as c:
        yield c

def test_get_status_count_valid_range(client, mongo_fixture):
    """
    Test the /status_count/ endpoint with a valid time range.
    Insert sample data into MongoDB and ensure the endpoint returns the correct counts.
    """
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
    """
    Test the /status_count/ endpoint with a time range that has no data.
    Ensure the endpoint returns an empty dictionary.
    """
    # No data inserted

    start_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
    end_time = (datetime.utcnow() + timedelta(days=2)).isoformat()

    response = client.get(f"/status_count/?start_time={start_time}&end_time={end_time}")

    assert response.status_code == 200
    assert response.json() == {}

def test_get_status_count_invalid_dates(client):
    """
    Test the /status_count/ endpoint with invalid date formats.
    Ensure the endpoint returns a 422 Unprocessable Entity status code.
    """
    # Invalid date formats

    invalid_data = [
        {"start_time": "invalid", "end_time": "invalid"},
        {"start_time": "2024-01-01", "end_time": "not-a-date"},
    ]

    for data in invalid_data:
        response = client.get(f"/status_count/?start_time={data['start_time']}&end_time={data['end_time']}")
        assert response.status_code == 422  # Unprocessable Entity
