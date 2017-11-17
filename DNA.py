from random import sample

class DNA:
    def __init__(self, length, mutationRate):
        self.__data = sample(range(length), length)
        self.__mutationRate = mutationRate

    def __str__(self):
        return ' '.join(str(x) for x in self.__data)

    def Print(self, path):
        file = open(path, 'w')
        file.write(str(self))
        file.close()