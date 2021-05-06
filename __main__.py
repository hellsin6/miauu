import websocket, time, binascii


def on_message(ws, packet):
	print(binascii.hexlify(packet))


def on_error(ws, error):
	print(error)


def on_close(ws):
	print("### closed ###")


def main():
    websocket.enableTrace(True)
    habbo_websocket = "wss://game-es.habbo.com:30001/websocket"
    ws = websocket.WebSocketApp(habbo_websocket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()


if __name__ == "__main__":
	main()