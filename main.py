from DNA import DNA
import os, re, sys
import json
#import plotly.plotly as py
#import plotly.graph_objs as go
#from datetime import datetime
#import pandas_datareader.data as web

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
    with open('./param.json') as data_file:
        params = json.load(data_file)
    #UniqueWords('./data/words-list.txt','./data/words-list-unique.txt')
    #SaveSenteses('./data/Newspapers', './data/sentences.txt')
    #sentences = ReadFile('./data/sentences.txt')
    #SaveUniqueWords(sentences, './data/words-from-sentences-unique.txt')
    words = ReadFile(params['sentences'])
    #words2 = ReadFile('./data/words-list-unique.txt')
    #words = list(set([words + words2]))
    words = [word for word in words if len(word) >= 3]
    print(len(words))
    with open(params['encoded-file'], 'r') as file:
        encoded = file.read()[:-1]
    print(encoded)
    count = params['population']
    length = params['length']
    mutation = params['mutation']
    if params['random'] == True:
        print('population: ', count)
        print('length: ', length)
        print('mutation: ', mutation)
        population = Population.Random(count, length, mutation, encoded, words)
    else:
        print ('continue with folder ', params['continue'])
        population = Population.FromFolder(params['continue'], count, length, mutation, encoded, words)
    
    while True:
        scores = population.CalcFitness()
        population.Print(params['print'])
        population.NaturalSelection()
