#  Games and Bayesian Classifiers
---
## Table of contents 
[Games and Bayesian Classifiers](#-1-games-and-bayesian-classifiers)
- [Part 1: Raichu](#part-1-raichu)
  - [1.1. Problem Statement](#11-problem-statement)
  - [1.2. Initial State](#12-initial-state)
  - [1.3. Successors](#13-successors)
  - [1.4. Utility function](#14-utility-function)
  - [1.5. ALpha beta pruning and Minimax](#15-alpha-beta-pruning-and-minimax)
  - [1.6. Conclusion](#16-conclusion)
- [Part 2: The Game of Quintris](#part-2-the-game-of-quintris)
  - [2.1. Problem Statement](#21-problem-statement)
  - [2.2. Initial State](#22-initial-state)
  - [2.3. Successors](#23-successors)
  - [2.4. Utility function](#24-utility-function)
  - [2.5. Search Algorithm](#25-search-algorithm)
- [Part 3: Truth be Told](#part-3-truth-be-told)
  - [3.1. Problem Statement](#31-problem-statement)
  - [3.2. Training Data Set](#32-training-data-set)
  - [3.3. Testing Data Set:](#33-testing-data-set)
  - [3.4. Prior probalitiy equation:](#34-prior-probalitiy-equation)
  - [3.5. Cleaning Dataset:](#35-cleaning-dataset)
  - [3.6. Liklihood probabilty:](#36-liklihood-probabilty)
  - [3.7. Naive Bayes Algorithm:](#37-naive-bayes-algorithm)
  - [3.8. Classification accuracy](#38-classification-accuracy)
---
## Part 1: Raichu
### 1.1. Problem Statement
Raichu refers to two player zero sum board game. It is a variation of checkers.As a part of assignment, Game AI / BOT need to be designed which can play a game. 

### 1.2. Initial State
Initial state is defined as initial configuaraion of game. It is not necessary to be start of a game but it can be any configuartion. It can be middle game or end game. 

### 1.3. Successors
Successors are defined for a given player as set of valid moves performed. It explores all possible legal moves for each pieces and return set of boards. 

### 1.4. Utility function
Utility function calculates scores based on current configuaration of game. It is currently defined as weighted difference of white and black peices on board. It is very basic utility fucntion and does not account for piece position on board. Also there are additional bonus points are given for peice position. It tries to control center as it is strategically very important to win.

### 1.5. Alpha beta pruning and Minimax
This utility function is used to generate game search tree. On serach tree we travedrse from depth =2 to depth = 11 and yields best move based on search. Due to time constraint, whichever board last configured is used as best move. Alpha beta pruning is used to improve efficiency of minimax search tree. Also, alpha beta pruning lot depends on how you arrange your deepest node. For this game, we arranged all captured move first and then all simpler moves. This way it improves pruning. Goal for white is to maximize while goal for black is to minimize the score. 

### 1.6. Conclusion
We initially used Minimax and then Alphabeta pruning. Alpha beta pruning definitely improved search and it was able to go upto depth 6 within 10 seconds of time. 

---

## Part 2: The Game of Quintris
### 2.1. Problem Statement
Quintris is a game of chance which is one player game. It works on maximizing score and hence expecitmax algorithm may be used. In this game random pieces falls to the game floor. User can move piece right or left, rotate or flip. If all columns of particular floor ids filled, it clears line. For each clear line user gets one point. Goal of the game is to maximize score. 

### 2.2. Initial State
Initial state of game is blank slate with pieces start to falling. it also shows what is next piece about to come. Score at initial state is zero.

### 2.3. Successors
Successors are defined for a given player as set of valid moves performed. It explores all possible legal moves for each pieces and return set of configuration. Branching factor can go up to 120. 

### 2.4. Utility function
There are several factors that are linearly combined to calculate utility function. It includes factors such as number holes at any given state, maximum height of column, bumpiness (it is defined as diffence of height between adjacent columns), number of pits which is defined as deep long holes etc. 

### 2.5. Search Algorithm
currently based on given utility function, it choses the successor with least cost and returns moves for that successors.

The game supports two versions viz -- human and computer. Each mode has animated and simple modes. The human version was already provided which is totally controlled by user. While the computer version is totally controlled by the AI and the moves are passed through Computer Player class and control_game method for animated mode and get_moves function from the same class for the simple mode.  

---
## Part 3: Truth be Told
### 3.1. Problem Statement
- The Bayes Classifier is a probabilistic model that makes the most probable prediction for a review in our case.

- It is described using the Bayes Theorem that provides a principled way for calculating a conditional probability.

- Using Bayes theorem, we can find the probability of A happening, given that B has occurred. Here, B is the evidence and A is the hypothesis. The assumption made here is that the predictors/features are independent. That is presence of one particular feature does not affect the other. Hence it is called naive.
  
- we are a dataset of user-generated reviews. User-generated
reviews are transforming competition in the hospitality industry, because they are valuable for both the guest and the hotel owner. 

- For the potential guest, it’s a valuable resource during the search for an overnight stay.
- For the hotelier, it’s a way to increase visibility and improve customer contact. So it really affects both the business and guest if people fake the reviews and try to either defame a good hotel or promote a bad one.

- Our task is to classify reviews into faked or legitimate, for 20 hotels in Chicago.

### 3.2. Training Data Set
- We are given a text file containing lines of reviews and a word at the beginning of the line giving us the information of the review following the word. The word is either truthful or deceptive.

### 3.3. Testing Data Set:
- The test is also similar to the training data set.

### 3.4. Prior probalitiy equation:

``` python
# Prior probabilities
prior_deceptive = math.log(deceptive_count_train) - math.log(deceptive_count_train+truthful_count_train)

prior_truthful = math.log(truthful_count_train) - math.log(deceptive_count_train+truthful_count_train)
```
- In the above code block has 2 prior probabilities, one for deceptive and the other for truthful.
- Both are take respective count in the training data set and total count in the traing data set.

### 3.5. Cleaning Dataset:
- Converted all the lines to lower case.
- Used the regex module to remove white spaces and special characters and anything that does not make sense.
- Created a list stop words which occour frequently as the part of grammer.
- Used the above list to ignore from sentence while building the model
``` python
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
```

### 3.6. Liklihood probabilty:
``` python
# Likelihood calculation for deceptive
    sum_deceptive = sum(deceptive_set.values())
    model = []
    for word in vocabulary:
        try:
            prob = math.log((deceptive_set[word] + 1)) - math.log(sum_deceptive)
        except KeyError:
            prob = math.log(1) - math.log(sum_deceptive)
        model.append("deceptive | " + word + " | %f\n" % prob)

    # Probability calculation for truthful
    sum_truthful = sum(truthful_set.values())
    for word in vocabulary:
        try:
            prob = math.log((truthful_set[word] + 1)) - math.log(sum_truthful)

        except KeyError:
            prob = math.log(1) - math.log(sum_truthful)
        model.append("truthful | " + word + " | %f\n" % prob)
```
- The above code created a list of strings with likelihood probabilties of each word in the dataset apart of stop words and catogerize them into two classes i.e truthful and deceptive.

### 3.7. Naive Bayes Algorithm:
- Before we start working on the given data the main function tweaks the test data by making a copy of the test data without the correct labels, so the classifier can't cheat!
  
``` python
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
```
- In the above code used we used the prior probablities caluclated and kept adding the respective truthful and deceptive probabilities and in the used them to predict output i.e if the review is truthful or deceptive

### 3.8. Result - Classification accuracy
Classification accuracy = 86.00%

---





