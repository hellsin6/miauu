from g_python.hpacket import HPacket
import socket, binascii, requests, struct, os

luftbb = requests.get("https://api.harble.net/messages/latest.json").json()
version = luftbb["Revision"]


def find_id(msg, type):
	for x in luftbb[type]:
		if x["Name"] == msg:
			return x["Id"]
	return None


def find_name(msg, type):
	for x in luftbb[type]:
		if x["Id"] == msg:
			return x["Name"]
	return None


def get_header(packet):
	header_id = struct.unpack(">h", packet[4:6])[0]
	return find_name(header_id, "Incoming")


def extract_diffie(packet):
	pointer = 6
	len_A = struct.unpack(">h", packet[pointer:pointer+2])[0]
	pointer += 2
	A = packet[pointer:pointer+len_A]

	pointer += len_A
	len_g = struct.unpack(">h", packet[pointer:pointer+2])[0]
	pointer += 2
	g = packet[pointer:pointer+len_g]

	return int(A, 16), int(g, 16)


def main():
	sck = socket.socket()
	sck.connect(("game-es.habbo.com", 30000))

	start = HPacket(find_id("ClientHello", "Outgoing"), version, "FLASH3", 1, 0)
	diffie = HPacket(find_id("InitDiffieHandshake", "Outgoing"))

	sck.send(bytes(start))
	sck.send(bytes(diffie))

	
	while True:
		data = sck.recv(1024)

		if len(data) > 0:
			print(get_header(data), data[6:])
		
			if get_header(data) == "ErrorReport":
				sck.close()
				exit()
			
			if get_header(data) == "InitDiffieHandshake":
				A, g = extract_diffie(data)
				N = int.from_bytes(os.urandom(256), "big")

				B = hex(pow(A, N, g))[2:]

				d_resp = HPacket(find_id("CompleteDiffieHandshake", "Outgoing"), B)
				sck.send(bytes(d_resp))

	sck.close()


if __name__ == '__main__':
	main()