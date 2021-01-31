import asyncio
from typing import List
from datetime import datetime, timedelta
from random import randrange

from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise

from .ble import Connection
from .constants import FEED_CHARACTERISTIC
from .models import Event, EventPydantic, ScheduleConfiguration

app = FastAPI(
    title="PiTutor",
    description="PetTutor API",
    version="0.1.0",
)

loop = asyncio.get_event_loop()
queue = asyncio.Queue()
connection = Connection(loop, FEED_CHARACTERISTIC)
start_event = asyncio.Event()
stop_event = asyncio.Event()

schedule_config = ScheduleConfiguration(
    initial_delay=600, interval_range_start=30, interval_range_end=30, timeout=3600
)


async def feed_queue_manager(connection: Connection, queue: asyncio.Queue):
    while True:
        if connection.client and connection.connected:
            await queue.get()
            await connection.client.write_gatt_char(FEED_CHARACTERISTIC, bytearray(0))
            print("Sent feed instruction.")
            await Event.create(name="FEED")
        else:
            await asyncio.sleep(2)


async def feed_scheduler(
    queue: asyncio.Queue, start_event: asyncio.Event, stop_event: asyncio.Event
):
    while True:
        await start_event.wait()
        await asyncio.wait(
            [stop_event.wait(), asyncio.sleep(schedule_config.initial_delay)],
            return_when=asyncio.FIRST_COMPLETED,
        )
        end_time = datetime.utcnow() + timedelta(seconds=schedule_config.timeout)
        while datetime.utcnow() < end_time:
            if stop_event.is_set():
                stop_event.clear()
                break
            queue.put_nowait(0)  # Feed
            await asyncio.wait(
                [
                    stop_event.wait(),
                    asyncio.sleep(
                        randrange(
                            schedule_config.interval_range_start,
                            schedule_config.interval_range_end,
                            5,
                        ),
                        loop=loop,
                    ),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
        start_event.clear()


@app.on_event("startup")
async def startup_event():
    asyncio.ensure_future(connection.manager())
    asyncio.ensure_future(feed_queue_manager(connection, queue))
    asyncio.ensure_future(feed_scheduler(queue, start_event, stop_event))


@app.on_event("shutdown")
async def shutdown_event():
    print("Disconnecting...")
    loop.run_until_complete(connection.cleanup())


@app.post("/api/feed", status_code=202)
async def feed():
    if all([queue, connection, connection.connected]):
        queue.put_nowait(0)


@app.post("/api/schedule/start", status_code=202)
async def start_schedule():
    start_event.set()


@app.post("/api/schedule/stop", status_code=202)
async def stop_schedule():
    stop_event.set()


@app.put("/api/schedule/configuration", status_code=201, response_model=ScheduleConfiguration)
async def set_schedule(configuration: ScheduleConfiguration):
    for key, val in configuration.dict().items():
        setattr(schedule_config, key, val)
    return schedule_config

@app.get("/api/schedule/configuration", response_model=ScheduleConfiguration)
async def get_schedule():
    return schedule_config

@app.get("/api/status")
async def status():
    return {
        "bluetooth": "Connected to PetTutor"
        if hasattr(connection, "client") and connection.connected
        else "Connecting...",
        "schedule": "On" if start_event.is_set() else "Off",
    }


@app.get("/api/events", response_model=List[EventPydantic])
async def get_events():
    return await EventPydantic.from_queryset(Event.all().order_by("-timestamp"))


register_tortoise(
    app,
    db_url="sqlite:///var/db/pitutor/db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)