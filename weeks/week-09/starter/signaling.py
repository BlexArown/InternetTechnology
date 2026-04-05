import asyncio
import websockets

CONNECTIONS = set()


async def handler(websocket):
    CONNECTIONS.add(websocket)
    print("Client connected. Total:", len(CONNECTIONS))

    try:
        async for message in websocket:
            dead_connections = []

            for conn in CONNECTIONS:
                if conn != websocket:
                    try:
                        await conn.send(message)
                    except Exception:
                        dead_connections.append(conn)

            for conn in dead_connections:
                CONNECTIONS.discard(conn)

    except Exception as e:
        print("Connection error:", e)

    finally:
        CONNECTIONS.discard(websocket)
        print("Client disconnected. Total:", len(CONNECTIONS))


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Signaling server started on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
