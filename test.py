import asyncio
import websockets

async def hello():
	uri = "ws://snubbyland.herokuapp.com/game/level"
	async with websockets.connect(uri) as websocket:
		a=1
		if a:
			await websocket.send("hello world")
			greeting = await websocket.recv()
			print(greeting)
		else:
			await websocket.send("@45 1")
			greeting = await websocket.recv()
			print(greeting)

asyncio.get_event_loop().run_until_complete(hello())