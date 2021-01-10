import csv
import time
import timeit

from lz78 import Lz78

if __name__ == '__main__':
    source_file = "source.txt"
    destination_file = "binary.txt"
    # lz78 = Lz78(source_file, destination_file, action_choice=action_choice, dictionary_capacity=dictionary_capacity)

    # time = timeit.timeit(stmt=lz78.encode, number=5)
    # print(time)

    # def tests():
    #     with open("results.csv", "w") as results:
    #         spamwriter = csv.writer(results, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #         for dictionary_capacity in range(0, 301, 100):
    #             for action_choice in range(0, 3):
    #                 lz78 = Lz78(source_file, destination_file, action_choice=action_choice, dictionary_capacity=dictionary_capacity)
    #                 text = lz78.encode()
    #                 time = timeit.timeit(stmt=lambda x: lz78.save_to_file(text), number=5)
    #                 spamwriter.writerow([action_choice, dictionary_capacity, time/5])
    # tests()

    action_choice = 0
    dictionary_capacity = 0
    # lz78 = Lz78(source_file, destination_file, action_choice=action_choice, dictionary_capacity=dictionary_capacity)
    # text = lz78.encode()
    # lz78.save_to_file(text)
    # print(text)
    # print(timeit.timeit(stmt=lambda: lz78.save_to_file(text), number=5))

    # encoded_text = lz78.encode()

    # encoded_text_from_file = lz78.get_encoded_text_from_file()
    print("READ")

    # with open("results.csv", "w") as results:
    #     spamwriter = csv.writer(results, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     for dictionary_capacity in range(0, 301, 100):
    #         for action_choice in range(0, 3):
    lz78 = Lz78(source_file, destination_file, action_choice=action_choice, dictionary_capacity=dictionary_capacity)
    text = lz78.encode()
                # print(lz78.encoder.result)
    lz78.save_to_file(text)
                # encoded_text_from_file = lz78.get_encoded_text_from_file()
                # print("dec")
                # start_time = time.time()
                # lz78.decode(encoded_text_from_file)
                # spamwriter.writerow([action_choice, dictionary_capacity, time.time() - start_time])

