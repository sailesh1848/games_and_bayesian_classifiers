# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#
import re
import math
import pandas as pd
from decimal import *
from collections import Counter
import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}



def get_token(sentence):
    '''
    THis functions generate tokens for given sentence/s. It removes certain stop
    words that does not contribute much to the learning. 

    List of stop words are collected from
     https://gist.github.com/sebleier/554280

     Apart from that if length of word is just one character or if word is not
     alpha it is ignored. 
    '''
    sentence = re.sub(r'[\r|\n|\r\n|.|,]+', ' ',sentence)
    sentence = re.sub((r'[^\w\s]'),'', sentence).lower() 
    sentence = re.sub((r'\d+'),'', sentence).lower()
    sentence = re.sub((r'_+'),'', sentence).lower()
    words = re.sub(r'[^\w\s]', ' ', sentence).split()
    stop_words = ["a", "about", "above", "after", "again", "against", "ain",
                  "all", "am", "an", "and", "any", "are", "aren", "aren't",
                  "as", "at", "be", "because", "been", "before", "being",
                  "below", "between", "both", "but", "by", "can", "couldn",
                  "couldn't", "d", "did", "didn", "didn't", "do", "does",
                  "doesn", "doesn't", "doing", "don", "don't", "down", "during",
                  "each", "few", "for", "from", "further", "had", "hadn",
                  "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't",
                  "having", "he", "her", "here", "hers", "herself", "him",
                  "himself", "his", "how", "i", "if", "in", "into", "is", "isn",
                  "isn't", "it", "it's", "its", "itself", "just", "ll", "m",
                  "ma", "me", "mightn", "mightn't", "more", "most", "mustn",
                  "mustn't", "my", "myself", "needn", "needn't", "no", "nor",
                  "not", "now", "o", "of", "off", "on", "once", "only", "or",
                  "other", "our", "ours", "ourselves", "out", "over", "own",
                  "re", "s", "same", "shan", "shan't", "she", "she's", "should",
                  "should've", "shouldn", "shouldn't", "so", "some", "such", "t",
                  "than", "that", "that'll", "the", "their", "theirs", "them",
                  "themselves", "then", "there", "these", "they", "this", "those",
                  "through", "to", "too", "under", "until", "up", "ve", "very",
                  "was", "wasn", "wasn't", "we", "were", "weren", "weren't",
                  "what", "when", "where", "which", "while", "who", "whom", "why",
                  "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you",
                  "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
                  "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's",
                  "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", 
                  "that's", "there's", "they'd", "they'll", "they're", "they've",
                  "we'd", "we'll", "we're", "we've", "what's", "when's", "where's",
                  "who's", "why's", "would"]
    tokens = [word for word in words if len(word) > 1 and word.isalpha() and word not in stop_words]
    return tokens


def readingInput(data):
    ## Function converts dictionary into dataframe
    df = pd.DataFrame(
        {
            'text':data["objects"],
            'label':data["labels"],
        }
    )
    df['text'] =df['text'].apply(lambda x: get_token(x))
    return df


def cal_prob(deceptive_set, truthful_set, truthful_count_train,
             deceptive_count_train, vocabulary):
    
    ''' This function calculates prior and likelihood of labels
    also ,we have used log function in order to avoid multiplication of very 
    small numbers. 

    WE also decide to use Laplace smoothing. Laplace smoothing adds one (1) to
    total count of word and hence if word is not in particular label, still
    classifier does not generate error.

    We have reference from https://www.youtube.com/watch?v=O2L2Uv9pdDA&t=201s
    '''

    # Prior probabilities
    prior_deceptive = math.log(deceptive_count_train) - math.log(deceptive_count_train+truthful_count_train)
    prior_truthful = math.log(truthful_count_train) - math.log(deceptive_count_train+truthful_count_train)

    # Likelihood calculation for deceptive
    sum_deceptive = sum(deceptive_set.values())
    model = []
    for word in vocabulary:
        try:
            prob = math.log((deceptive_set[word] + 1)) - math.log(sum_deceptive)
            # prob = (deceptive_set[word] + 1) / sum_deceptive
        except KeyError:
            prob = math.log(1) - math.log(sum_deceptive)
            # prob = (1) / sum_deceptive
        model.append("deceptive | " + word + " | %f\n" % prob)

    # Probability calculation for truthful
    sum_truthful = sum(truthful_set.values())
    for word in vocabulary:
        try:
            prob = math.log((truthful_set[word] + 1)) - math.log(sum_truthful)
            # prob = (truthful_set[word] + 1) / sum_truthful

        except KeyError:
            prob = math.log(1) - math.log(sum_truthful)
            # prob = (1) / sum_truthful
        model.append("truthful | " + word + " | %f\n" % prob)

    return model,prior_deceptive,prior_truthful     

def read_learned_model(trained_model):
    ## This function assigns likelihood of given word in their respective labels
    truthful_dict = dict()
    deceptive_dict = dict()

    for data in trained_model:
        data = data.split(" | ")
        if data[0] == 'truthful':
                truthful_dict[data[1]] = Decimal(data[2])
        elif data[0] == 'deceptive':
                deceptive_dict[data[1]] = Decimal(data[2])
    
    return  truthful_dict, deceptive_dict

def naive_bayes(test_df, prior_deceptive,
                prior_truthful, truthful_dict, deceptive_dict):
    
    '''
    core code behind classifier. It is noted that we have ignored denominator
    from bayes law as here we are comparing posterior probability of two labesl
    and denominator will always be same. 
    '''
    output = []
    # print(len(truthful_dict), len(deceptive_dict))
        
    # print(test_df['text'][0])
    for wordlist in test_df['text']:
        truthful_val = Decimal(prior_truthful)
        deceptive_val = Decimal(prior_deceptive)
        for word in wordlist:
            if word in truthful_dict.keys() :
                truthful_val += Decimal(truthful_dict[word])
            if word in deceptive_dict.keys():
                deceptive_val += Decimal(deceptive_dict[word])
        if truthful_val > deceptive_val:
            output.append("truthful")
        else:
            output.append("deceptive")

    return output

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):

    '''
    Main classifier
    reads train and test data, calls helper functions and generates predictions
    based on Naive bayes
    '''


    train_df = readingInput(train_data)
    test_df = readingInput(test_data).drop('label', axis=1)

    truthful_count_train = train_df['label'].value_counts()['truthful']
    deceptive_count_train = train_df['label'].value_counts()['deceptive']

    vocabulary = set(train_df['text'].sum())

    deceptive_set = Counter(train_df[train_df['label'] =='deceptive'].sum()[0])
    truthful_set = Counter(train_df[train_df['label'] =='truthful'].sum()[0])

    trained_model,prior_deceptive,prior_truthful = cal_prob(deceptive_set, truthful_set,
                                                    truthful_count_train,
                                                     deceptive_count_train,
                                                     vocabulary)
    


    truthful_dict, deceptive_dict = read_learned_model(trained_model)

    output = []

    for wordlist in test_df['text']:
        truthful_val = Decimal(prior_truthful)
        deceptive_val = Decimal(prior_deceptive)
        for word in wordlist:
            if word in truthful_dict.keys() :
                truthful_val += Decimal(truthful_dict[word])
            if word in deceptive_dict.keys():
                deceptive_val += Decimal(deceptive_dict[word])
        if truthful_val > deceptive_val:
            output.append("truthful")
        else:
            output.append("deceptive")

    predicted_data = naive_bayes(test_df, prior_deceptive,prior_truthful,
                                 truthful_dict, deceptive_dict)
    return predicted_data


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
