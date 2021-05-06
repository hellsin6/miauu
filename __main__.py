from g_python.hpacket import HPacket
import socket, binascii


def main():
    client_socket = socket.socket()
    client_socket.connect(("game-es.habbo.com", 30000))

    # {ClientHello}{s:"WIN63-202104221206-601649277"}{s:"FLASH3"}{i:1}{i:0}
    start = HPacket(4000, "WIN63-202104221206-601649277", "FLASH3", 1, 0)
    diffie = HPacket(2329)

    client_socket.send(bytes(start))
    client_socket.send(bytes(diffie))

    data = client_socket.recv(1024)
    if len(data) > 0:
        print(binascii.b2a_hex(data))
        client_socket.send(bytes(HPacket(2346)))

    client_socket.close()


if __name__ == '__main__':
    main()