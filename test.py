import asyncio
import websockets

async def hello():
	uri = "ws://snubbyland.herokuapp.com/game/level"
	async with websockets.connect(uri) as websocket:
		a=0
		if a:
			L="""22 serialization::archive 16 22 serialization::archive 16 0 1 0
0 12 20 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 20 0 0 0 0 -1 1 2 1 2 1 2 1 2 1 2 1 0 0 0 0 20 0 0 0 0 -1 2 1 2 1 2 1 2 1 2 1 -1 0 0 0 0 20 0 0 0 0 -1 1 2 1 2 1 2 1 2 1 2 -1 0 0 0 0 20 0 0 0 0 -1 2 1 2 1 2 1 2 1 2 1 -1 0 0 0 0 20 0 0 0 0 -1 1 2 1 2 1 2 1 2 1 2 -1 0 0 0 0 20 0 0 0 0 -1 2 1 2 1 2 1 2 1 2 1 -1 0 0 0 0 20 0 0 0 0 -1 1 2 1 2 1 2 1 2 1 2 -1 0 0 0 0 20 0 0 0 0 -1 2 1 2 1 2 1 2 1 2 1 -1 0 0 0 0 20 0 0 0 0 2 1 2 1 2 1 2 1 2 1 2 -1 0 0 0 0 20 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 20 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 0 0 1 0 0 0 810 330 0 0 155 315 0 0 9 0 0 0 0 0 301 482 704 484 705 440 301 440 300 401 703 399 704 360 302 360 299 322 703 318 703 281 302 279 300 245 702 240 700 201 302 199 300 161 701 155 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5.00000000000000000e+02 5.00000000000000000e+02 1.00000000000000000e+02 1.00000000000000000e+02
"""
			await websocket.send(L)
			greeting = await websocket.recv()
			print(greeting)
		else:
			await websocket.send("LL146")
			greeting = await websocket.recv()
			print(greeting)

asyncio.get_event_loop().run_until_complete(hello())