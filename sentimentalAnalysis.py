import random
import string

from nltk.corpus import twitter_samples
from nltk.tag import pos_tag, pos_tag_sents
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist
import nltk
import pandas as pd
import numpy as np
import re

''' Clean data function '''
def cleanLabel(rate):
    rate = rate[0:3]
    return rate
def cleanData(data):
    data = re.sub(r'!','',data)
    data = re.sub(r'“', '', data)
    data = re.sub(r'“', '', data)
    return data

''' Using nltk function to divide the sentence'''
def divideSentence(comment):
    sentence = nltk.sent_tokenize(comment)
    words = []
    for sent in sentence:
        word = nltk.word_tokenize(sent)
        for w in word:
            words.append(w)
    return words

def counterNumOfWords(words):
    fdist = FreqDist(words)
    tops = fdist.most_common(50)
    return tops

def fenci(file):
    return twitter_samples.tokenized(file)


def cleaned_list_func(evert_tweet):
    new_text = []
    cixing_list = pos_tag(evert_tweet)
    for word, cixing in cixing_list:
        word = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:[0-9a-fA-F][0-9a-fA-F]))+', '', word)
        word = re.sub('(@[A-Za-z0-9_]+)', '', word)
        if cixing.startswith('NN'):
            pos = 'n'
        elif cixing.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = WordNetLemmatizer()
        new_word = lemmatizer.lemmatize(word, pos)
        if len(new_word) > 0 and new_word not in string.punctuation and new_word.lower() not in stopwords.words(
                'english'):
            new_text.append(new_word.lower())
    return new_text


def get_all_words(clean_tokens_list):
    for tokens in clean_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(clean_tokens_list, tag):
    li = []
    for every_tweet in clean_tokens_list:
        data_dict = dict([token, True] for token in every_tweet)
        li.append((data_dict, tag))
    return li


def train_model(train_data):
    from nltk import NaiveBayesClassifier
    model = NaiveBayesClassifier.train(train_data)
    return model


def test(test_text):
    from nltk.tokenize import word_tokenize
    custom_tokens = cleaned_list_func(word_tokenize(test_text))
    result = dict([token, True] for token in custom_tokens)
    return result


if __name__ == '__main__':
    # nltk.download('twitter_samples')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('stopwords')
    # nltk.download('punkt')

    ##load data
    po_file_path = 'positive_tweets.json'
    ne_file_path = 'negative_tweets.json'

    positive_tweets = twitter_samples.strings(po_file_path)
    negative_tweets = twitter_samples.strings(ne_file_path)
    # for i in range(6):
    #     print(positive_tweets[i])
    #     print(negative_tweets[i])

    #分词
    po_fenci_res = fenci(po_file_path)
    be_fenci_res = fenci(ne_file_path)

    # print('Positive participle result: {}'.format(po_fenci_res))
    # print('Negative participle result: {}'.format(be_fenci_res))


    positive_cleaned_list = []
    negative_cleaned_list = []
    for i in po_fenci_res:
        positive_cleaned = cleaned_list_func(i)
        positive_cleaned_list.append(positive_cleaned)
    for j in be_fenci_res:
        negative_cleaned = cleaned_list_func(j)
        negative_cleaned_list.append(negative_cleaned)
    # print('Positive tweet results after processing: {}'.format(positive_cleaned_list))
    # print('original data: {}'.format(positive_tweets[:2]))

po_for_model = get_tweets_for_model(positive_cleaned_list, 'Positive')
ne_for_model = get_tweets_for_model(negative_cleaned_list, 'Negative')
print('positive data: {}'.format(po_for_model))
print('negative data: {}'.format(ne_for_model))

model_data = po_for_model + ne_for_model
random.shuffle(model_data)

train_data = model_data[:7000]
test_data = model_data[7000:]

model = train_model(train_data)

''' Get and clean data '''
data = []
with open('climb.csv', 'r', encoding='utf-8') as origin_data:
    header = True
    for line in origin_data:
        if(header):
            header = False
        else:
            data.append(list(line.strip().lower().split('\t')))
dataset = pd.DataFrame(data)
dataset[1] = dataset[1].apply(cleanLabel)
dataset[0] = dataset[0].apply(cleanData)

results = []
labels = []
for index, row in dataset.iterrows():
    result = test(dataset.iloc[index].iat[0])
    results.append(model.classify(result))
    if float(dataset.iloc[index].iat[1]) >= 3:
        labels.append(1)
    else:
        labels.append(0)

for i in range(len(results)):
    if results[i] == 'Positive':
        results[i] = 1
    else:
        results[i] = 0
print(results)

dataset[2] = results
dataset[3] = labels
print(dataset)

error = 0
count = 0
for index, row in dataset.iterrows():
    if dataset.iloc[index].iat[2] != dataset.iloc[index].iat[3]:
        error = error + 1
    count = count + 1
accuray = 1-error/count
print("Accuray: ",accuray)
