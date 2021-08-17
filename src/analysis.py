# analysis.py - processing the tweets
#
# Author: Daniel Choo
# Date:   11/17/20
# URL:    https://www.github.com/kyoogoo/twump

import re
import json
import random
from pathlib import Path, PurePath
from nltk import classify, data, download
from nltk.corpus import twitter_samples, stopwords
from nltk.sentiment import SentimentAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentIntensityAnalyzer


class Analysis:
    def __init__(self):
        """ __init__(self):

            Return(s):    None [None]
        """
        self.stopwords = {"RT"}
        self.check()

    def check(self):
        """ check(self):
            Checks if NLTK modules are installed.

            Returns(s):   None [None]
        """
        try:
            data.find('vader_lexicon')
        except LookupError:
            download('vader_lexicon')

        try:
            data.find('stopwords')
        except LookupError:
            download('stopwords')

        try:
            data.find('twitter_samples')
        except LookupError:
            download('twitter_samples')

    def cleanup(self, tweets):
        """ cleanup(self, user_tweets):
            Removing some unnecessary parts of our tweets.
            Some things we will be removing include links, some stopwords,
            twitter handles, and other punctuation.

            Return(s):    None [None]
        """
        # Initializing variable(s)
        i = 0
        stop = set(stopwords.words('english'))

        # Iterate over the tweets
        for tweet in tweets:
            # Some processing on our strings.
            print(tweet)
            temp = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
            temp = re.sub(r'@[^\s]+', '', temp)
            temp = list(filter(lambda x: not x in self.stopwords, temp.split()))

            # Init. counter var.
            counter = 0

            # Filter out stopwords
            for j in temp:
                if j in stop:
                    temp.pop(counter)
                counter += 1

            # Make our list back into a singular string.
            s = ' '.join(temp)
            s = (s.encode('ascii', 'ignore')).decode("utf-8")

            tweets[i] = s
            i+=1

    def sentiment(self):
        """ sentiment(self):
            Conducting sentiment analysis on the tweets that we have
            scraped for the purposes of seeing if the person typically
            posts positive, negative, or neutral tweets.

            Return(s):    None [None]
        """
        # Retrieve the user they would like to calculate this on
        username = str(input("Please provide the user: "))

        # Initializing necessary variables.
        filename = username + ".json"
        path = PurePath(Path("").absolute().parent, Path("data/tweets/" + filename))
        user_tweets = []

        # Open the requested user's already scraped tweets.
        with open(path, "r") as file:
            data = json.load(file)
            for i in data:
                user_tweets.append(i.get('full_text'))

        # Removing unnecessary words
        self.cleanup(user_tweets)

        # Pre-trained sentiment analysis library
        sia = SentimentIntensityAnalyzer()

        # Print out the scores
        for i in user_tweets:
            print(i)
            print(sia.polarity_scores(i))
            print()

        # I'll come back to training my own model :')
        """
        pos = twitter_samples.strings('positive_tweets.json')
        neg = twitter_samples.strings('negative_tweets.json')

        counter = 0
        for i in pos:
            s = " ".join(i)
            pos[counter] = s
            counter+=1

        print(pos)

        counter = 0
        for i in neg:
            s = " ".join(i)
            neg[counter] = s
            counter+=1

        self.cleanup(pos)
        self.cleanup(neg)

        pos_test = [{tweet: "Positive"} for tweet in pos]
        neg_test = [{tweet, "Negative"} for tweet in neg]

        # Create our test set
        testing = pos_test + neg_test
        random.shuffle(testing)

        # Train our own model
        model = NaiveBayesClassifier.train(testing)
        print("Accuracy is:", classify.accuracy(model, testing))
        print(user_tweets, model.classify(dict([token, True] for token in user_tweets)))
        """

    def menu(self):
        """ menu(self):
            Providing the user a menu to traverse.
            1.) Sentiment
                - Time to conduct sentiment analysis! Will take in one user
                  and see whether their tweets are positive, negative, or
                  neutral.

            2.) Comparing the sentiment between two users' tweets
                - donkey

            2.) Return to main menu
                - Does as expected, will return to the main menu
                  and prompt the user either to scrape, conduct analysis
                  or exit the program.

            Return(s):    None [None]
        """
        # Initializing vars.
        input_flag = False
        menu_check = [1,2]

        # Infinite loop until break.
        while True:
            while not input_flag:
                try:
                    print("\nAnalysis Menu:\n1.) Calculate sentence similarity\n2.) Return to main menu")
                    usr_input = int(input("\nEnter your choice: "))
                    if usr_input in menu_check:
                        input_flag = True

                # Invalid input.
                except ValueError:
                    print("\nInvalid input. Proper responses: 1, 2, 3 (integers)")

            if usr_input == 1:
                self.sentiment()
            else:
                return
            input_flag = False
