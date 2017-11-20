from DNA import DNA
import os, re
import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime
import pandas_datareader.data as web

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
                total = total + [''.join(list(filter(lambda x: str.isalpha(x) or x == ' ', str.lower(sentence)))) for sentence in sentences]
    myFile = open(toFile, 'w')
    for sentence in total:
        print(sentence, file = myFile)
def decode(encode, path):
    with open(path) as file:
        data = [int(x) for x in file.read().split()]  # read first line
    decoded = ''
    for value in encoded:
        decoded = decoded + chr(data[ord(value)- ord('a')] + ord('a'))
    return  decoded

def ReadFile(file):
    with open(file, 'r') as f:
        lines = [line[:-1] for line in f]
    return lines

def SaveUniqueWords(sentences, toFile):
    for sentence in sentences:
        print(sentence)
    print(len(sentences))
    words = set()
    for sentence in sentences:
        for word in sentence.split():
            words.add(word)
    myFile = open(toFile, 'w')
    for word in words:
        print(word, file = myFile)

if __name__ == '__main__':
    #UniqueWords('./data/words-list.txt','./data/words-list-unique.txt')
    #SaveSenteses('./data/Newspapers', './data/sentences.txt')
    #sentences = ReadFile('./data/sentences.txt')
    #SaveUniqueWords(sentences, './data/words-from-sentences-unique.txt')
    words = ReadFile('./data/words-from-sentences-unique.txt')
    words = [word for word in words if len(word) >= 2]
    print(len(words))
    with open('./data/encoded-file.txt', 'r') as file:
        encoded = file.read()[:-1]
    print(encoded)
#    for i in range(470):
#        print(decode(encoded, './generation/2/' + str(i) + '.txt'))
#    exit(0)
    #population = Population.FromFile('./generation/best', 470, 26, 0, encoded, words)
    population = Population.Random(1000, 26, 0.01, encoded, words)
    generation = 1
    while True:
        scores = population.CalcFitness()
        population.Print(generation)
        population.NaturalSelection()
        generation = generation + 1
