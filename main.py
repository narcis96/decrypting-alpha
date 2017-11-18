from DNA import DNA
import os, re
from Population import Population

def UniqueWords(fromFile, toFile):
    with open(fromFile, 'r') as f:
        listWords = [line[:-1] for line in f]
    myFile = open(toFile, 'w')
    for word in list(set(listWords)):
        print(word,file = myFile)

def SaveSenteses(path, toFile):
    total = []
    for file in os.listdir(path):
        if file.endswith('.r'):
            with open(path + "/" + file, 'r', encoding = 'utf-8', errors='ignore') as content_file:
                sentences = re.split(r'[!?.]+',content_file.read())
                total = total + [''.join(list(filter(str.isalpha, str.lower(sentence)))) for sentence in sentences]
    myFile = open(toFile, 'w')
    for sentence in total:
        print(sentence, file = myFile)

def ReadFile(file):
    with open(file, 'r') as f:
        lines = [line[:-1] for line in f]
    return lines

if __name__ == '__main__':
    #UniqueWords('./data/words-list.txt','./data/words-list-unique.txt')
    #SaveSenteses('./data/Newspapers', './data/sentences.txt')
    words = ReadFile('./data/words-list-unique.txt')
    sentences = ReadFile('./data/sentences.txt')
    print(len(words))
    print(len(sentences))
    with open('./data/encoded-file.txt', 'r') as file:
        encoded = file.read()[:-1]
    print(encoded)
    print(encoded)

    population = Population.FromFile('./generation/37',470, 26, 0.1, encoded, words, )
    generation = 1
    while True:
        scores = population.CalcFitness()
        population.Print(generation)
        population.MatingPool()
        population.NaturalSelection()
        generation = generation + 1
