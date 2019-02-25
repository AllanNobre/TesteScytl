import socket
from BitsConversionTable import conversionTable4to5


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
        self.receive_message()

    def create_socket_connection(self):
        self.soc.connect((IP_ADRESS, PORT))

    def receive_message(self):
        self.input_message = self.soc.recv(RECEIVE_BUFFER_SIZE)

    def organize_packets(self):
        self.packets = []
        bytes_count = 5
        tmp_bytes_vector = []

        for byte in self.input_message:
            if chr(byte) == START_PACKET_HEX and bytes_count == 5:
                print(str(chr(byte)))
                bytes_count = 0
                tmp_bytes_vector = []
            elif chr(byte) == END_PACKET_HEX and bytes_count == 5:
                print(str(chr(byte)))
                self.packets.append(tmp_bytes_vector)
                pass
            elif chr(byte) == END_TRANSMISSION_HEX and bytes_count == 5:
                print(str(chr(byte)))
                self.packets.append(tmp_bytes_vector)
                pass
            else:
                bytes_count += 1
                tmp_bytes_vector.append(bin(byte)[2:].zfill(8))

        print(self.packets)


def test_print(connection):
    for a in connection.input_message:
        if chr(a) == START_PACKET_HEX:  # hex(int("11000110", 2)):
            print("INICIO -------------")

        if chr(a) == END_PACKET_HEX:  # hex(int("11000110", 2)):
            print("MEIO -------------")

        if chr(a) == END_TRANSMISSION_HEX:  # hex(int("11000110", 2)):
            print("FIM -------------")

        print("Inteiro {}  -  Binário {}  -  Hexadecimal {}".format(a, bin(a), hex(a)))

    for key, val in conversionTable4to5.items():
        print("Key 4 Bits: {}  -  Value 5 Bits: {}".format(key, val))


if __name__ == "__main__":
    connection = Connection()
    connection.organize_packets()
    test_print(connection)
