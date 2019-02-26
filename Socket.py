import socket
from BitsConversionTable import conversionTable4to5


IP_ADRESS = "189.6.76.118"
PORT = 50080
RECEIVE_BUFFER_SIZE = 500
START_PACKET_HEX = "\xC6"  # Hexadecimal start value 0xC6 (11000110)
END_PACKET_HEX = "\x6B"  # Hexadecimal end packet value 0x6B (01101011)
END_TRANSMISSION_HEX = "\x21"  # Hexadecimal end connection value 0x21 (00100001)
START_PACKET_BIN = "11000110"  # Binary start value
END_PACKET_BIN = "01101011"  # Binary end packet value
END_TRANSMISSION_BIN = "00100001"  # Binary end connection value
LARGEST_PRIME_FACTOR = "00000101"  # Binary value to largest prime factor of 50080 that fit in a byte, that is 5


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

        for byte in self.input_message:
            if chr(byte) == START_PACKET_HEX and bytes_count == 5:
                bytes_count = 0
                tmp_bytes_vector = []
            elif chr(byte) == END_PACKET_HEX and bytes_count == 5:
                self.packets_8_bits.append(tmp_bytes_vector)
                pass
            elif chr(byte) == END_TRANSMISSION_HEX and bytes_count == 5:
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

    def convert_5_bits_into_4_bits(self):
        self.packets_4_bits = []

        for packet in self.packets_5_bits:
            tmp_byte_vector = []

            for block_5_bit in packet:
                block_4_bit = self.find_4_bit_block_corresponding(block_5_bit)
                tmp_byte_vector.append(block_4_bit)

            self.packets_4_bits.append(tmp_byte_vector)

    def find_4_bit_block_corresponding(self, block_5_bit):
        for table_block_4_bit, table_block_5_bit in conversionTable4to5.items():
            if table_block_5_bit == block_5_bit:
                return table_block_4_bit

    def mount_decoded_message(self):
        self.decoded_message = ""

        for packet in self.packets_4_bits:
            tmp_bits_string = ""
            block_transform = False

            for block_4_bits in packet:
                if block_transform:
                    tmp_bits_string += block_4_bits

                    self.decoded_message += self.transform_byte_into_ASCII(tmp_bits_string)

                    tmp_bits_string = ""
                    block_transform = False
                else:
                    tmp_bits_string = block_4_bits
                    block_transform = True

    def transform_byte_into_ASCII(self, tmp_bits_string):
        byte = int(tmp_bits_string, 2)

        return str(chr(byte))

    def decode_message(self):
        self.organize_packets_in_8_bits()
        self.organize_packets_in_5_bits()
        self.convert_5_bits_into_4_bits()
        self.mount_decoded_message()

    def treat_message(self):
        # Removing any trailing spaces
        decoded_message = self.decoded_message
        decoded_message = decoded_message.rstrip()

        # Changing odd characters to lower case and the upper even
        treated_message = ""
        for index in range(0, len(decoded_message)):
            if index % 2 == 1:
                treated_message += decoded_message[index].lower()
            else:
                treated_message += decoded_message[index].upper()

        # Switching spaces to underline
        treated_message = treated_message.replace(" ", "_")

        # Inverting message
        treated_message = treated_message[::-1]

        self.treated_message = treated_message

    def handling_message_lenght(self):
        message = self.treated_message
        message_lenght = len(message)

        # Padding right with underlines to turn message lenght divisible by 4 if needed
        if message_lenght % 4 != 0:
            number_of_underlines = 4 - message_lenght % 4

            for index in range(number_of_underlines):
                message += "_"

        self.treated_message = message.encode("ASCII")

    def organize_message_in_byte_blocks(self):
        self.packets_8_bits_to_send = []
        tmp_bytes_vector = []

        for byte in self.treated_message:
            if len(tmp_bytes_vector) != 4:
                tmp_bytes_vector.append(bin(byte)[2:].zfill(8))
            else:
                self.packets_8_bits_to_send.append(tmp_bytes_vector)
                tmp_bytes_vector = []
                tmp_bytes_vector.append(bin(byte)[2:].zfill(8))

        self.packets_8_bits_to_send.append(tmp_bytes_vector)

    def organize_packets_in_4_bits_blocks(self):
        self.packets_4_bits_to_send = []

        # Concatenating the bits in a string to divide it into 8 pieces with 4-Bit
        for packet in self.packets_8_bits_to_send:
            tmp_bits_string = ""
            tmp_bits_vector = []
            bit_slice = ""

            for byte in packet:
                tmp_bits_string += byte

            for bit in tmp_bits_string:
                if len(bit_slice) != 4:
                    bit_slice += bit
                else:
                    tmp_bits_vector.append(bit_slice)
                    bit_slice = ""
                    bit_slice += bit

            tmp_bits_vector.append(bit_slice)

            self.packets_4_bits_to_send.append(tmp_bits_vector)

    def convert_4_bits_into_5_bits(self):
        self.packets_5_bits_to_send = []

        for packet in self.packets_4_bits_to_send:
            tmp_byte_vector = []

            for block_4_bit in packet:
                block_5_bit = conversionTable4to5.get(block_4_bit)
                tmp_byte_vector.append(block_5_bit)

            self.packets_5_bits_to_send.append(tmp_byte_vector)

    def organize_message_in_byte_blocks_encodeds(self):
        self.packets_8_bits_encodeds_to_send = []

        # Concatenating the bits in a string to divide it into 8 pieces with 4-Bit
        for packet in self.packets_5_bits_to_send:
            tmp_bits_string = ""
            tmp_byte_vector = []
            bit_slice = ""

            for byte in packet:
                tmp_bits_string += byte

            for bit in tmp_bits_string:
                if len(bit_slice) != 8:
                    bit_slice += bit
                else:
                    tmp_byte_vector.append(bit_slice)
                    bit_slice = ""
                    bit_slice += bit

            tmp_byte_vector.append(bit_slice)

            self.packets_8_bits_encodeds_to_send.append(tmp_byte_vector)

    def apply_xor_in_bytes(self):
        self.packets_with_xor = []
        largest_prime_factor_byte = int(LARGEST_PRIME_FACTOR, 2)

        for packet in self.packets_8_bits_encodeds_to_send:
            tmp_byte_vector = []

            for binary_byte in packet:
                byte = int(binary_byte, 2)
                tmp_byte_vector.append(bin(byte ^ largest_prime_factor_byte)[2:].zfill(8))

            self.packets_with_xor.append(tmp_byte_vector)

    def mount_encoded_message(self):
        self.encoded_message = "".encode("ASCII")
        message_packets_count = len(self.packets_with_xor)

        for index in range(0, message_packets_count):
            self.encoded_message += int(START_PACKET_BIN, 2).to_bytes(1, byteorder='big')

            for byte in self.packets_with_xor[index]:
                self.encoded_message += int(byte, 2).to_bytes(1, byteorder='big')

            if index == message_packets_count - 1:
                self.encoded_message += int(END_TRANSMISSION_BIN, 2).to_bytes(1, byteorder='big')
            else:
                self.encoded_message += int(END_PACKET_BIN, 2).to_bytes(1, byteorder='big')

    def send_message(self):
        self.soc.send(self.encoded_message)

    def encode_message(self):
        self.handling_message_lenght()
        self.organize_message_in_byte_blocks()
        self.organize_packets_in_4_bits_blocks()
        self.convert_4_bits_into_5_bits()
        self.organize_message_in_byte_blocks_encodeds()
        self.apply_xor_in_bytes()
        self.mount_encoded_message()


if __name__ == "__main__":
    connection = Connection()
    connection.decode_message()
    connection.treat_message()
    connection.encode_message()
    connection.send_message()
