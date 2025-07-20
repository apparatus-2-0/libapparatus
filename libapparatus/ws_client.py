import asyncio
import json
import websockets

import libapparatus


class WSClient:
    def __init__(self, host="localhost", port=8100, topic=None, message_handler=None, on_connect=None, reconnect_delay=3, debug=False):
        self.uri = f"ws://{host}:{port}/websocket"
        self.name = f"WSClient:{topic}" if topic else "WSClient"
        self.ws = None
        self.message_handler = message_handler
        self.on_connect = on_connect
        self.listen_task = None
        self.reconnect_delay = reconnect_delay
        self._stop = False
        self.logger = libapparatus.get_logger(name=self.name, debug=debug)

    async def connect(self):
        while not self._stop:
            try:
                self.ws = await websockets.connect(self.uri)
                if self.ws.state == websockets.protocol.State.OPEN:
                    self.logger.info(f"Connected to {self.uri}")
                    if self.on_connect:
                        if asyncio.iscoroutinefunction(self.on_connect):
                            await self.on_connect()
                        else:
                            self.on_connect(self)
                    self.logger.info(f"Connected to {self.uri}")
                    self.listen_task = asyncio.create_task(self.listen())
                    await self.listen_task  # Wait until listen returns (connection lost)
            except Exception as e:
                self.logger.error(f"Websocket connection error: {e}. reconnecting in {self.reconnect_delay}s...")
                await asyncio.sleep(self.reconnect_delay)

    async def send(self, message):
        """Sends a JSON-RPC 2.0 message over the websocket."""
        if not isinstance(message, dict):
            raise ValueError("Message must be a dictionary")
        if not message.get("jsonrpc") or message.get("jsonrpc") != "2.0":
            raise ValueError("Message must be a valid JSON-RPC 2.0 message with 'jsonrpc' key set to '2.0'")
        if not message.get("method"):
            raise ValueError("Message must be a valid JSON-RPC 2.0 message with 'method' key set")
        if not message.get("id"):
            raise ValueError("Message must be a valid JSON-RPC 2.0 message with 'id' key set")
        # Wait until the websocket is connected before sending
        while not (self.ws and self.ws.state == websockets.protocol.State.OPEN):
            if self._stop:
                return
            self.logger.warning("Websocket not connected, waiting to send message...")
            await asyncio.sleep(self.reconnect_delay)
        self.logger.debug(f"> {json.dumps(message)}")
        await self.ws.send(json.dumps(message))

    async def listen(self):
        try:
            async for message in self.ws:
                if self.message_handler:
                    await self.message_handler(message)
        except websockets.ConnectionClosed:
            pass  # Connection lost, will reconnect in connect()
        except Exception as e:
            self.logger.error(f"Websocket listen error: {e}")

    async def close(self):
        self._stop = True
        if self.ws:
            await self.ws.close()
        if self.listen_task:
            self.listen_task.cancel()
