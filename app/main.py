import asyncio
from typing import List

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

from .ble import Connection
from .constants import FEED_CHARACTERISTIC
from .models import Event, EventPydantic

templates = Jinja2Templates(directory="web/dist")

app = FastAPI(
    title="PiTutor",
    description="PetTutor API",
    version="0.1.0",
)

loop = asyncio.get_event_loop()
queue = asyncio.Queue()
connection = Connection(loop, FEED_CHARACTERISTIC)


async def feed_queue_manager(connection: Connection, queue: asyncio.Queue):
    while True:
        if connection.client and connection.connected:
            await queue.get()
            await connection.client.write_gatt_char(FEED_CHARACTERISTIC, bytearray(0))
            print("Sent feed instruction.")
            await Event.create(name="FEED")
        else:
            await asyncio.sleep(2.0, loop=loop)


@app.on_event("startup")
async def startup_event():
    asyncio.ensure_future(connection.manager())
    asyncio.ensure_future(feed_queue_manager(connection, queue))


@app.on_event("shutdown")
async def shutdown_event():
    print("Disconnecting...")
    loop.run_until_complete(connection.cleanup())


@app.get("/feed")
async def feed():
    if all([queue, connection, connection.connected]):
        queue.put_nowait(0)
    return "done."


@app.get("/api/status")
async def status():
    return {
        "bluetooth": "Connected to PetTutor"
        if hasattr(connection, "client") and connection.connected
        else "Connecting..."
    }


@app.get("/api/events", response_model=List[EventPydantic])
async def get_events():
    return await EventPydantic.from_queryset(Event.all())


@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.mount("/", StaticFiles(directory="web/dist"), name="web")

register_tortoise(
    app,
    db_url="sqlite:///var/db/pitutor/db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)