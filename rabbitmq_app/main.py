# server/app/main.py
from fastapi import FastAPI
from routes import router
from process_rabbitmq_data import start_mqtt_consumer

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup_event():
    import threading
    threading.Thread(target=start_mqtt_consumer, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
