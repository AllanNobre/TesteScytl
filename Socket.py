import socket
from BitsConversionTable import conversionTable4to5


IP_ADRESS = "189.6.76.118"
PORT = 50080
RECEIVE_BUFFER_SIZE = 500
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

    def organize_packets_in_8_bits(self):
        self.packets_8_bits = []
        bytes_count = 5
        tmp_bytes_vector = []

        for byte in self.input_message:
            if chr(byte) == START_PACKET_HEX and bytes_count == 5:
                print(str(chr(byte)))
                bytes_count = 0
                tmp_bytes_vector = []
            elif chr(byte) == END_PACKET_HEX and bytes_count == 5:
                print(str(chr(byte)))
                self.packets_8_bits.append(tmp_bytes_vector)
                pass
            elif chr(byte) == END_TRANSMISSION_HEX and bytes_count == 5:
                print(str(chr(byte)))
                self.packets_8_bits.append(tmp_bytes_vector)
                pass
            else:
                bytes_count += 1
                tmp_bytes_vector.append(bin(byte)[2:].zfill(8))

    def organize_packets_in_5_bits(self):
        self.packets_5_bits = []

        # Concatenating the bits in a string to divide it into 8 pieces with 5-Bit
        for packet in self.packets_8_bits:
            tmp_bits_string = ""
            tmp_bits_vector = []
            bit_slice = ""

            for byte in packet:
                tmp_bits_string += byte

            for bit in tmp_bits_string:
                if len(bit_slice) != 5:
                    bit_slice += bit
                else:
                    tmp_bits_vector.append(bit_slice)
                    bit_slice = ""
                    bit_slice += bit

            tmp_bits_vector.append(bit_slice)

            self.packets_5_bits.append(tmp_bits_vector)

    def decode_message(self):
        self.organize_packets_in_8_bits()
        self.organize_packets_in_5_bits()


def test_print(connection):
    print("================TESTE===============")
    print(connection.packets_8_bits)
    print(connection.packets_5_bits)

    for a in connection.input_message:
        if chr(a) == START_PACKET_HEX:  # hex(int("11000110", 2)):
            print("INICIO -------------")

        if chr(a) == END_PACKET_HEX:  # hex(int("11000110", 2)):
            print("MEIO -------------")

        if chr(a) == END_TRANSMISSION_HEX:  # hex(int("11000110", 2)):
            print("FIM -------------")

        print("Inteiro {}  -  Binário {}  -  Hexadecimal {}".format(a, bin(a), hex(a)))

    # for key, val in conversionTable4to5.items():
    #     print("Key 4 Bits: {}  -  Value 5 Bits: {}".format(key, val))

    # print("================CONVERSAO===============")
    # a = connection.packets_8_bits[0][0]
    # print(a)

    # b = int(a, 2)
    # print(b)

    # print(str(chr(b)))

    # bit_mask = int('11110000', 2)

    # print(bin(bit_mask & b)[2:].zfill(8))


if __name__ == "__main__":
    connection = Connection()
    connection.decode_message()
    test_print(connection)
