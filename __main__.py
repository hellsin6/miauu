from g_python.hpacket import HPacket
import socket, binascii, requests

luftbb = requests.get("https://api.harble.net/messages/latest.json").json()
latest_version = luftbb["Revision"]


def find_id(msg, type):
	for x in luftbb[type]:
		if x["Name"] == msg:
			return x["Id"]


def main():
	client_socket = socket.socket()
	client_socket.connect(("game-es.habbo.com", 30000))

	start = HPacket(find_id("ClientHello", "Outgoing"), latest_version, "FLASH3", 1, 0)
	diffie = HPacket(find_id("InitDiffieHandshake", "Outgoing"))

	client_socket.send(bytes(start))
	client_socket.send(bytes(diffie))

	data = client_socket.recv(1024)
	if len(data) > 0:
		print(binascii.b2a_hex(data))
		client_socket.send(bytes(HPacket(2346)))

	client_socket.close()


if __name__ == '__main__':
	main()