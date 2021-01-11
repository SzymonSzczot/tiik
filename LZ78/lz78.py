import os
import re
from collections import OrderedDict


class Lz78Interface:

    def __init__(self, action, capacity):
        self.DICTIONARY_OVERLOAD_ACTION = {
            0: lambda act: self.clear_dictionary(),
            1: lambda act: self.delete_first(),
            2: lambda act: self.delete_last()
        }

        self.buffer_dictionary = OrderedDict()
        self.dictionary_capacity = capacity
        self.action_if_overload = self.DICTIONARY_OVERLOAD_ACTION.get(action)
        self.counter = 1

        self.overload_counter = 0

        self.result = []

    def handle_overflow(self):
        if self.dictionary_overflow():
            self.action_if_overload(True)

    def dictionary_overflow(self):
        if self.dictionary_capacity != 0 or self.counter > 4000:
            return len(self.buffer_dictionary) / 2 * 5 >= self.dictionary_capacity
        return False

    def clear_dictionary(self):
        self.buffer_dictionary.clear()
        self.reset_indexes()

    def delete_first(self):
        self.buffer_dictionary.popitem(last=False)
        self.overload_counter += 1
        self.counter = self.overload_counter
        if self.overload_counter > 4000:
            self.overload_counter = 1

    def delete_last(self):
        self.buffer_dictionary.popitem(last=True)
        self.counter -= 1

    def reset_indexes(self):
        self.counter = 1


class Encoder(Lz78Interface):

    def __init__(self, action, capacity):
        super().__init__(action, capacity)

    def LZ78_encode(self, data):
        previous = ""
        for letter in data:
            self.handle_overflow()
            previous = self.update_previous(previous, letter)
        if previous:
            self.consume_last_letter(previous)
        return self.result

    def update_previous(self, previous, letter):
        if previous + letter not in self.buffer_dictionary:
            previous = self.stream_not_in_dict(previous, letter)
        else:
            previous += letter
        return previous

    def stream_not_in_dict(self, previous, letter):
        if previous == "":
            self.sign_appear_first_time(letter)
        else:
            self.stream_already_in_dictionary(previous, letter)
        return self.reset_loop()

    def sign_appear_first_time(self, sign):
        self.result.append((0, sign))
        self.buffer_dictionary[sign] = self.counter

    def stream_already_in_dictionary(self, previous, letter):
        self.result.append((self.buffer_dictionary[previous], letter))
        self.buffer_dictionary[previous + letter] = self.counter

    def reset_loop(self):
        self.counter += 1
        return ""

    def consume_last_letter(self, previous):
        if self.buffer_dictionary[previous]:
            self.result.append((self.buffer_dictionary[previous], "0"))
        else:
            self.result.append((self.buffer_dictionary[previous], previous))


class Decoder(Lz78Interface):

    def __init__(self, action, capacity):
        super().__init__(action, capacity)

    def LZ78_decode(self, data):
        for part in Utils.get_equal_parts(data, 2, len(data)):
            index, letter = part
            self.handle_part(index, letter)
            self.handle_overflow()
        return ''.join(self.result).rstrip("0")

    def handle_part(self, index, letter):
        if index == 0:
            self.save_new_letter(letter)
        else:
            self.get_stream_from_dict(index, letter)

    def save_new_letter(self, letter):
        self.result.append(letter)
        self.buffer_dictionary[self.counter] = letter
        self.counter += 1

    def get_stream_from_dict(self, index, letter):
        self.result.append(self.buffer_dictionary[index] + letter)
        self.buffer_dictionary[self.counter] = self.buffer_dictionary[index] + letter
        self.counter += 1


class Lz78:

    def __init__(self, source_file, destination_file, action_choice=0, dictionary_capacity=0):
        self.encoder = Encoder(action_choice, dictionary_capacity)
        self.decoder = Decoder(action_choice, dictionary_capacity)
        self.utils = Utils()
        self.stats = Stats()
        self.status = 0

        self.source_file = source_file
        self.destination_file = destination_file

    def encode(self):
        source_text = self.get_text_to_encode()
        return self.encoder.LZ78_encode(source_text)

    def get_text_to_encode(self):
        with open(self.source_file, "r", encoding="utf-8") as file:
            return re.sub(r'[^\x00-\x7F]+', '', file.read())

    def save_to_file(self, encoded_pairs):
        with open(self.destination_file, "w") as file:
            file.write("")
        with open(self.destination_file, "ba") as file:
            for x in self.utils.get_equal_parts(encoded_pairs, 50_000, len(encoded_pairs)):
                try:
                    file.write(self.get_bytes_to_write(x))
                except:
                    import pdb;pdb.set_trace()

    def get_bytes_to_write(self, encoded_pairs):
        result = b''
        for four in self.utils.make_fours(encoded_pairs):
            self.status += 1
            result += self.utils.pack_to_bin(four, encoded_pairs)
        return result

    def get_encoded_text_from_file(self):
        to_decode = []
        self.status = 0
        with open(self.destination_file, "rb") as file:
            for pack in self.utils.get_equal_parts(file.read(), 5, self.stats.get_file_size(file)):
                pack = self.utils.bin_to_pack(pack)
                self.status += 1
                to_decode += pack
        return to_decode

    def decode(self, encoded_pairs):
        return self.decoder.LZ78_decode(list(pair for pair in encoded_pairs))


class Stats:

    @staticmethod
    def get_file_size(file):
        return file.seek(0, os.SEEK_END)


class Utils:

    def pack_to_bin(self, pack, encoded_pairs) -> bytes:
        encoded_pairs.append(pack)
        first, second = pack
        first_index, first_letter = first
        second_index, second_letter = second
        arr = [
            int(first_index) << 28,
            ord(first_letter) << 20,
            int(second_index) << 8,
            ord(second_letter)
        ]
        res = sum(arr)
        return res.to_bytes(5, byteorder="big")

    def bin_to_pack(self, bin_data: bytes):
        bytes_to_decode = int.from_bytes(bin_data, "big")
        part1 = bytes_to_decode >> 28

        moved_bytes = part1 << 28
        reduced_bytes = bytes_to_decode - moved_bytes
        part2 = reduced_bytes >> 20

        moved_bytes = part2 << 20
        reduced_bytes = reduced_bytes - moved_bytes
        part3 = reduced_bytes >> 8

        moved_bytes = part3 << 8
        reduced_bytes = reduced_bytes - moved_bytes
        part4 = reduced_bytes

        return part1, chr(part2), part3, chr(part4)

    def make_fours(self, data: list):
        part = self.get_equal_parts(data, 2, len(data))
        for p in part:
            if len(p) < 2:
                p.append((0, "0"))
            yield p

    @staticmethod
    def get_equal_parts(source: iter, part_length, source_length):
        return [source[x:x + part_length] for x in range(0, source_length, part_length)]
