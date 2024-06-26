from fastapi import FastAPI

# Import routers and data processing functions from their respective locations
from Assignment_rabbitmqt_upswing.rabbitmq_app.routes import router  # Assuming routes are defined here
from Assignment_rabbitmqt_upswing.rabbitmq_app.process_rabbitmq_data import start_mqtt_consumer  # Assuming data processing happens here

# Create a FastAPI application instance
app = FastAPI()

# Include the router defined in the `routes.py` file (adjust path if needed)
app.include_router(router)

# Define an event handler that runs on application startup
@app.on_event("startup")
async def startup_event():
    """
    This function starts the RabbitMQ consumer in a separate thread
    on application startup.
    """

    import threading
    # Create a background thread to run the consumer function
    consumer_thread = threading.Thread(target=start_mqtt_consumer, daemon=True)
    consumer_thread.start()

# Entry point for running the application (assuming uvicorn is used)
if __name__ == "__main__":
    import uvicorn
    # Configure and run the uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8002)
