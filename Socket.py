import socket


IP_ADRESS = "189.6.76.118"
PORT = 50080
RECEIVE_BUFFER_SIZE = 100
START_PACKET_HEX = "\xC6"  # Hexadecimal start value 0xC6 (11000110)
END_PACKET_HEX = "\x6B"  # Hexadecimal start value 0x6B (01101011)
END_TRANSMISSION_HEX = "\x21"  # Hexadecimal start value 0x21 (00100001)


class Connection:
    def __init__(self):
        self.soc = socket.socket()
        self.create_socket_connection()

    def create_socket_connection(self):
        self.soc.connect((IP_ADRESS, PORT))

    def receive_message(self):
        input_message = self.soc.recv(RECEIVE_BUFFER_SIZE)

        return input_message


if __name__ == "__main__":
    connection = Connection()
    input_message = connection.receive_message()
    print(type(input_message))

    for a in input_message:
        if chr(a) == START_PACKET_HEX:  # hex(int("11000110", 2)):
            print("Inicio")

        if chr(a) == END_PACKET_HEX:  # hex(int("11000110", 2)):
            print("MEIO")

        if chr(a) == END_TRANSMISSION_HEX:  # hex(int("11000110", 2)):
            print("FIM")

        print(type(a))
        print(bin(a))
        print(hex(a))
