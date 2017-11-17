from DNA import DNA


class Population:
    def __init__(self, count, length, mutationRate):
        self.__data = [DNA(length, mutationRate) for i in range(count)]

    def Print(self, path):
        print(len(self.__data))
        for i,dna in enumerate(self.__data) :
            dna.Print(path + str(i) + '.txt')

