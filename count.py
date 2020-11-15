import math
from collections import Counter

files = ["polski.txt", "informatyczny.txt", "angielski.txt"]

for file_name in files:

    with open(file_name, "r") as file:
        text = file.read()
        counts = Counter(text)
        all_letters = len(text)
        print(file_name)
        print(counts)
        print(all_letters)
        enthropies = {}
        for letter, count in counts.items():
            p = count/all_letters
            enthropies[letter] = abs(p*math.log(p, 2) + (1-p)*math.log(1-p, 2))
        ent = sorted(enthropies.items(), key=lambda x: -x[1])
        print(ent)
        with open("res_" + file_name, "w") as writeable:
            for i, y in ent:

                writeable.write(str(i) + " " + str(y) + "\n")
