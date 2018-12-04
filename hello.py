import pandas as pd

###################
#importing dataset#
###################

data = pd.read_csv('Report.csv', error_bad_lines=False)
data_text = data[['short_desc']]
data_text['index'] = data_text.index
documents = data_text


####################
#importing packages#
####################
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem import PorterStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')

ps = PorterStemmer()


######################
#preprocess functions#
######################


def lemmatize_stemming(text):
    return ps.stem(text)
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result



############################################
#preprocess documents and create dictionary#
############################################

processed_docs = documents['short_desc'].map(preprocess)
dictionary = gensim.corpora.Dictionary(processed_docs)


##########################################################################
#dictionary filter which i used, 25 is calculated, freq greater than 1100#
##########################################################################

dictionary.filter_n_most_frequent(25)



#####################
#useless, just print#
#####################
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break



#############################################################
#dictionary filter, may be used later but not worked for now#
#############################################################

#dictionary.filter_extremes(no_above=4.5, keep_n=500000)




##########################
#dictionary to bow corpus#
##########################

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]


##################
#word frequencies#
##################

word_freq = []
for j in range(len(bow_corpus)):
    bow_doc_4310 = bow_corpus[j]
    for i in range(len(bow_doc_4310)):
        if(bow_doc_4310[i][0] > len(word_freq)-1):
            word_freq.append(bow_doc_4310[i][1])
        else:
            word_freq[bow_doc_4310[i][0]] = word_freq[bow_doc_4310[i][0]] + bow_doc_4310[i][1]

import csv

Freq_data = open('WordFreq.csv', 'w')

csvwriter = csv.writer(Freq_data)
Freq_head = []
Freq_head.append('id')
Freq_head.append('word')
Freq_head.append('freq')
csvwriter.writerow(Freq_head)



for j in range(len(bow_corpus)):
    bow_doc_4310 = bow_corpus[j]
    for i in range(len(bow_doc_4310)):
        Freq_row = []
        Freq_row.append(bow_doc_4310[i][0])
        Freq_row.append(dictionary[bow_doc_4310[i][0]])
        Freq_row.append(word_freq[bow_doc_4310[i][0]])
        csvwriter.writerow(Freq_row)


Freq_data.close()



################
#lda and topics#
################


from gensim import corpora, models

tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
from pprint import pprint
for doc in corpus_tfidf:
    pprint(doc)
    break


lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} Words: {}'.format(idx, topic))


print("\n")
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=20, id2word=dictionary, passes=2, workers=4)

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))



###############
#default tests#
###############


unseen_document = ' PostgreSQL seems to incorrectly detect control characters... or clean_text() incorrectly fixes them PostgreSQL incorrectly detects that some summaries have control characters when they don'
bow_vector = dictionary.doc2bow(preprocess(unseen_document))
for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, index))


unseen_document = 'forwarding email message crashes thunderbird'
bow_vector = dictionary.doc2bow(preprocess(unseen_document))
for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, index))


unseen_document = 'Spelling mistake in docs, section Searching for Bugs'
bow_vector = dictionary.doc2bow(preprocess(unseen_document))
for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, index))


######################
## bug topic scores ##
######################

#greater than 200#
developer_num_list = []
developer_name_list = []

import csv
with open('Developers.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        if int(row['Num of Bugs']) > 200:
            print(row['developer'], row['Num of Bugs'])
            developer_name_list.append(row['developer'])


class Report:
    reports = []
    def __init__(self, bugId, shortDesc, developer):
        self.bugId = bugId
        self.shortDesc = shortDesc
        self.developer = developer
        Report.reports.append(self)

with open('Report.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['developer'] in developer_name_list:
            Report(row['id'], row['short_desc'], row['developer'])


Scores_data = open('Scores.csv', 'w')

csvwriter = csv.writer(Scores_data)
Scores_head = []
Scores_head.append('developer')
#Scores_head.append('short_desc')
Scores_head.append('topic0')
Scores_head.append('topic1')
Scores_head.append('topic2')
Scores_head.append('topic3')
Scores_head.append('topic4')
Scores_head.append('topic5')
Scores_head.append('topic6')
Scores_head.append('topic7')
Scores_head.append('topic8')
Scores_head.append('topic9')
csvwriter.writerow(Scores_head)

for report in Report.reports:
    short_desc = report.shortDesc
    bow_vector = dictionary.doc2bow(preprocess(short_desc))
    Scores_row = []
    Scores_row.append(report.developer)
    #Scores_row.append(report.bugId)
    print("Developer: {}\t Short Desc: {}".format(report.developer, report.shortDesc))
    counter = 0
    for i in range(10):
        Scores_row.append(0)

    for index, score in lda_model[bow_vector]:
        Scores_row[index+1] = score
        print("Score: {}\t Topic: {}".format(score, index))

    csvwriter.writerow(Scores_row)

Scores_data.close()


##benim##
from sklearn.model_selection import StratifiedKFold

df = pd.read_csv("Scores.csv")

X = np.array(df.iloc[:, 1:11])
y = np.array(df.iloc[:,0])

skf = StratifiedKFold(n_splits=10)

skf.get_n_splits(X,y)

from sklearn import svm
from sklearn.svm import SVC

class Probs:
    probs = []
    def __init__(self, prob, dev):
        self.prob = prob
        self.dev = dev
        Probs.probs.append(self)

results = []
for train_index, test_index in skf.split(X, y):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    clf = svm.SVC(gamma='scale', decision_function_shape='ovo', probability=True).fit(X_train, y_train)
    probs = clf.predict_proba(X_test)

    correct_count = 0
    fail_count = 0
    for testInd in range(len(probs)):

        Probs.probs = []

        for index, prob in enumerate(probs[testInd]):
            Probs(prob, clf.classes_[index])
    
        Probs.probs.sort(key=lambda Probs: Probs.prob, reverse=True)


        predictions = []

        i = 0

        for i in range(10):
            predictions.append(Probs.probs[i].dev)



        if y_test[testInd] in predictions:
            correct_count = correct_count + 1
        else:
            fail_count = fail_count + 1

    results.append(correct_count / (correct_count + fail_count))
    print(correct_count / (correct_count + fail_count))

    #clf = svm.SVC(gamma='scale', decision_function_shape='ovo').fit(X_train, y_train)
    #clf.score(X_test, y_test)
    
sum = 0
for i in range(len(results)):
    sum = sum + results[i]


average = sum / len(results)