import os
import re
from sys import getsizeof
from textwrap import wrap


class Encoder:

    DICTIONARY_OVERLOAD_ACTION = {
        "MAKE_NEW_DICT": "0"
    }

    def __init__(self, action, capacity):

        self.buffer_dictionary = {}
        dictionary_capacity = capacity
        dictionary_type = self.DICTIONARY_OVERLOAD_ACTION.get(action, "0")

    def LZ78_encode(self, data):
        counter = 1
        previous = ""
        result = ""
        for letter in data:
            # print(buffer_dictionary)
            # print(previous, letter)
            if previous + letter not in self.buffer_dictionary:
                if previous == "":
                    # specjalny przypadek: symbol
                    # nie występuje jeszcze w słowniku
                    result += self.to_bytes((0, letter))
                    self.buffer_dictionary[letter] = counter
                    # print(getsizeof(buffer_dictionary))
                else:
                    # ciąg 'c' jest w słowniku
                    result += self.to_bytes((self.buffer_dictionary[previous], letter))
                    self.buffer_dictionary[previous + letter] = counter
                counter += 1
                previous = ''
            else:
                previous += letter

        if previous:
            if self.buffer_dictionary[previous]:
                result += self.to_bytes((self.buffer_dictionary[previous], ))
            else:
                result += self.to_bytes((self.buffer_dictionary[previous], previous))
        # print(buffer_dictionary)
        return result

    def to_bytes(self, phrases):
        ret = ""
        for phrase in phrases:
            ret += str(phrase)
        return ret


def LZ78_decode(data):
    D = {}
    n = 1

    result = []
    for xs in get_equal_parts(data, 2, len(data)):
        i, s = xs
        if i == "0":
            result.append(s)
            D[str(n)] = s
            n = n + 1
        else:
            result.append(D[i] + s)
            D[str(n)] = D[i] + s
            n = n + 1
    return ''.join(result)


def pack_to_bin(pack: str) -> bytes:
    try:
        assert len(pack) == 4
    except AssertionError:
        while len(pack) != 4:
            pack += "0"
    print(pack)
    first_index, first_letter, second_index, second_letter = pack
    try:
        arr = [
            int(first_index) << 28,
            ord(first_letter) << 20,
            int(second_index) << 8,
            ord(second_letter)
        ]
    except:
        import pdb;pdb.set_trace()
    res = sum(arr)
    return res.to_bytes(5, byteorder="big")


def bin_to_pack(bin_data: bytes) -> str:
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

    return str(part1) + chr(part2) + str(part3) + chr(part4)


def make_pairs(data: str) -> list:
    return wrap(data, 4)


def get_equal_parts(source: iter, part_length, source_length):
    return [source[x:x + part_length] for x in range(0, source_length, part_length)]


if __name__ == '__main__':
    with open("test_text.txt", "r", encoding="utf-8") as file:
        to_encode = file.read()
        to_encode = re.sub(r'[^\x00-\x7F]+', '', to_encode)
    # to_encode = "sdfgadsfjklfas"

    encoder = Encoder("1", 100)
    test = encoder.LZ78_encode(to_encode)

    # test = "1a4b3p6v"
    result = b''
    with open("binary.txt", "wb") as f:
        for x in make_pairs(test):
            result += pack_to_bin(x)
        f.write(result)
    x = ""
    with open("binary.txt", "rb") as f:
        bs = f.read()
        file_size = f.seek(0, os.SEEK_END)
        for pack in get_equal_parts(bs, 5, file_size):
            pack = bin_to_pack(pack)
            x += "".join(i for i in get_equal_parts(pack, 2, len(pack)))
        print(LZ78_decode(list(y for y in x)))



    # # print(result)
    # with open("test.txt", "w", encoding="ascii") as file:
    #     file.write(result)
    # decoded = LZ78_decode(result)
    # print(decoded)
