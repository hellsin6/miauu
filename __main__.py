import websocket, time, binascii, struct


def on_open(ws):
	print("# Connected")


def on_close(ws):
	print("# Disconnected")


def on_error(ws, error):
	print(error)


def on_message(ws, packet):
	length = struct.unpack(">i", packet[:4])[0]
	header = struct.unpack(">h", packet[4:6])[0]

	body = binascii.hexlify(packet[6:]) if len(packet) > 6 else b""

	print(length, header, body)


def main():
	habbo_websocket = "wss://game-es.habbo.com:30001/websocket"
	ws = websocket.WebSocketApp(habbo_websocket,
								on_open=on_open,
								on_message=on_message,
								on_error=on_error,
								on_close=on_close)

	ws.run_forever()


if __name__ == "__main__":
	main()