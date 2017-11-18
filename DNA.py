from random import sample, random, randint


class DNA:

    def __init__(self, data, mutationRate, encoded, words):
        self.__data = data
        self.__mutationRate = mutationRate
        self.__score = 0
        self.__encoded = encoded
        self.__words = words

    @classmethod
    def Random(cls, length, mutationRate, encoded, words):
        return cls(sample(range(length), length), mutationRate, encoded, words)

    @classmethod
    def FromFile(cls, path, length, mutationRate, encoded, words):
        with open(path) as file:
            data = [int(x) for x in file.read().split()]  # read first line
        return cls(data, mutationRate, encoded, words)

    def __str__(self):
        return ' '.join(str(x) for x in self.__data)

    def Print(self, path):
        file = open(path, 'w')
        file.write(str(self))
        file.close()

    def CrossOver(self, fromFirst, other):
        data = [0] * len(self.__data)
        for i,value in enumerate(self.__data):
            if random() < fromFirst:
                data[i] = value
            else:
                data[i] = other.__data[i]

            if random() < self.__mutationRate:
                data[i] = randint(0, len(self.__data))

        return DNA(data, self.__mutationRate, self.__encoded, self.__words)

    def GetScore(self):
        return self.__score

    def CalcFitness(self):
        decoded = ''
        for value in self.__encoded:
            decoded = decoded + chr(self.__data[ord(value)- ord('a')] + ord('a'))
        score = 0
        for word in self.__words:
            if word in decoded:
                score += 1
        self.__score = pow(score, 3)
