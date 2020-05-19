import asyncio
import websockets

async def hello():
    uri = "ws://snubbyland.herokuapp.com/game/stream"
    async with websockets.connect(uri) as websocket:
        await websocket.send("@5454 1")
        greeting = await websocket.recv()
        print(greeting)

asyncio.get_event_loop().run_until_complete(hello())