def LZ78_encode(data):
    D = {}
    n = 1
    c = ''
    result = []
    for s in data:
        print(D)
        if c + s not in D:
            if c == '':
                # specjalny przypadek: symbol 's'
                # nie występuje jeszcze w słowniku
                result.append((0, s))
                D[s] = n
            else:
                # ciąg 'c' jest w słowniku
                result.append((D[c], s))
                D[c + s] = n
            n = n + 1
            c = ''
        else:
            c = c + s

    return result


def LZ78_decode(data):
    D = {}
    n = 1

    result = []
    for i, s in data:
        if i == 0:
            result.append(s)
            D[n] = s
            n = n + 1
        else:
            result.append(D[i] + s)
            D[n] = D[i] + s
            n = n + 1

    return ''.join(result)


if __name__ == '__main__':
    import sys
    from math import log, ceil

    data = open("test_text.txt", encoding="utf-8").read()
    comp = LZ78_encode(data)
    print(comp)
    decomp = LZ78_decode(comp)

    k = len(comp)
    n = int(ceil(log(max(index for index, symbol in comp), 2.0)))

    l1 = len(data)
    l2 = (k * (n + 8) + 7) / 8

    print("Liczba par: %d" % k)
    print("Maks. liczba bitów potrzebna do zapisania kodu: %d" % n)
    print("Maks. liczba bitów potrzebna do zapisania pary: %d + %d = %d" % (n, 8, n + 8))
    print("Rozmiar danych wejściowych: %d bajtów" % l1)
    print("Rozmiar danych skompresowanych: %d bajtów" % l2)
    print("Stopień kompresji: %.2f%%" % (100.0 * (l1 - l2) / l1))
    # print data
    # print decomp