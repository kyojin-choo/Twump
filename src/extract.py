# extract.py - scraping twitter
#
# Author: Daniel Choo
# Date:   10/28/19
# URL:    https://www.github.com/kyoogoo/twump

import os
import sys
import json
import tweepy
from pathlib import Path, PurePath


class Extract:
    def __init__(self):
        self.VALID = ["", "y", "n", "yes", "no"]
        self.YES = ["", "y", "yes"]
        self.NO = ["n", "no"]

    def authorize(self):
        """ authorize(): Reads in credentials JSON; verifies login. If the credentials files does not exist, create a
                     template for the user.

            Return:      N/A (sys.exit if file is missing)
        """
        secret = {"ACCESS_KEY":      None,
                  "ACCESS_SECRET":   None,
                  "CONSUMER_KEY":    None,
                  "CONSUMER_SECRET": None}

        values = ["ACCESS_KEY", "ACCESS_SECRET", "CONSUMER_KEY", "CONSUMER_SECRET"]
        path = PurePath(Path("").absolute().parent, Path("credentials.json"))

        # If the file (credentials.json) exists...
        if Path(path).exists():
            # Open file and read in the json information.
            with open(path) as cred:
                data = json.load(cred)
                counter = 0
                # Appending the values into secret dict.
                for key in secret:
                    secret[key] = data[values[counter]]
                    counter += 1

            # Checking OAuth authentication...
            try:
                auth = tweepy.OAuthHandler(secret["CONSUMER_KEY"], secret["CONSUMER_SECRET"])
            except tweepy.RaiseError:
                print("\nError: Invalid consumer key! Exiting Program.\n")
                sys.exit(-1)

            # Checking access_token...
            try:
                auth.set_access_token(secret["ACCESS_KEY"], secret["ACCESS_SECRET"])
            except tweepy.RaiseError:
                print("\nError: Invalid access token! Exiting Program.\n")
                sys.exit(-1)

            # Success! Ensure we are running a JSON parser.
            api = tweepy.API(auth)
            print("\n✧･ﾟ Authorized! ✧･ﾟ")
            print("Logged in as: " + str(api.me().screen_name))
            return api

        # If the file does not exist...
        else:
            path = PurePath(Path("").absolute().parent, Path("credentials_template.json"))
            # If the credentials.json is missing and the template exists, typo?
            if Path(path).exists():
                print("\nYou have either not properly named your file to 'credentials.json'")
                print("Or there may be a typo in the file name. Else, this error should not be occurring.")
            else:
                # If the credentials.json and template do not exist, create it!
                with open(path, "w") as file:
                    file.write(json.dumps(secret, indent=4))
                    print("\nCreated new credentials template.\nHowever, you are missing the necessary file to proceed.")
                    print("Please fill in the blanks with the necessary information.")
                    print("Also, please rename the template file to 'credentials.json'")
            sys.exit(-1)


    def print_tweet(self, status):
        """ print_tweet(status): just prints the tweet text (void function)
            Return:              N/A (void)
        """
        if 'retweeted_status' in status._json:
            print("\n" + str(status.created_at) + ": " + status._json['retweeted_status']['full_text'])
        else:
            print("\n" + str(status.created_at) + ": " + status.full_text)


    def getUser(self, api):
        """ getUser(username): retrieves user input from the user and 
            Return:            user (API object)
        """
        # Attempt to see if the user exists on Twitter.
        while True:
            user_input = -1
            print("\nNOTE: You can only scrape the most recent ~3,000 Tweets from a user.")
            print("Input 'self' to scrape your own timeline | Input nothing to exit.\n")
            username = str(input("Enter the Twitter Account to scrape: "))
            try:
                # Use streaming API on my own Twitter feed
                if username == "self":
                    print("myself")
                    sys.exit(0)
                elif username == "":
                    sys.exit(0)
                # Use REST API on user's twitter timeline
                else:
                    user = api.get_user(username)

            # If username does not exist, retry or exit.
            except tweepy.TweepError:
                print("\nThat user does not exist.")
                while user_input not in range(0, 2):
                    user_input = int(input("0 to exit, 1 to retry: "))

                if user_input == 1:
                    continue
                else:
                    print("\nBye!")
                    sys.exit(-1)
            # If we successfully retrieve a user, leave the loop.
            else:
                break

        return user


    def write(self, path, tweets):
        """ write():   Writes the array of Tweets into a JSON formatted file.
            Return:    N/A
        """
        try:
            with open(path, "w+") as file:
                file.write(json.dumps(tweets, indent=4, ensure_ascii=False))
        except Exception as ex:
            print("Whoopsie daisies, something went wrong!. This is the error: " + ex)


    def extract(self, api, username):
        """ extract(): Extracting data from Twitter (REST API)
                       It will print out the messages it scrapes and append
                       them into a JSON file.
            Return:    N/A [None]: void
        """
        # Formatting file path; initializing variables.
        filename = username + ".json"
        path = PurePath(Path("").absolute().parent, Path("data/tweets/" + filename))
        check = False
        date = ""
        tweet_count = 0
        tweets = []
        combined = []

        # Printing message, but also boolean value flips if the file exists. Required for loading JSON.
        # Note: You are not allowed to extract more than 3,000 tweets without a enterpise developer's account.
        if Path(path).exists():
            # Input checking
            while True:
                try:
                    exists = str(input("\nPath exists already. Would you like to scrape up to the last scraped tweet? (yes): "))
                    if exists in self.VALID:
                        break
                except ValueError:
                    print("\nInvalid input. Proper responses: '', 'y', 'n', 'yes', 'no'\n")

            # Lets scrape newer tweets!
            if exists in self.YES:
                print("\nScraping to the most recently obtained tweet.")
                print("Most recent tweet: ", end='')

                # Initializing relevant variables.
                new_count = 0
                to_id = 0

                with open(path, "r") as file:
                    data = json.load(file)
                    to_id = data[0].get('id')
                    print(data[0].get('full_text'))

                # Time to scrape some new tweets!
                for status in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items():
                    # If the curr ID = target ID, break.
                    try:
                        if status.id == to_id:
                            break
                        else:
                            self.print_tweet(status)
                            tweets.append(status._json)
                            new_count += 1
                    except Exception:
                        print("Oopsies woopsies. Error block: lines 194-204")

                combined = tweets + data
                del data, tweets          # Rudimentary memory handling. Lists easily 40MB+.
                self.write(path, combined)     # Writing to file.

                # Pretty print; inquire user if they want to scrape again.
                if new_count == 0:
                    print("\n\n✧･ﾟ@" + username + " has not tweeted any new tweets!･ﾟ･✧\n")
                    return
                else:
                    print("\n\n✧･ﾟ@" + username + " has tweeted " + str(new_count) + " more tweets since the last scrape!･ﾟ･✧\n")
                    return

            # Don't want to scrape new tweets :( Reprompt to scrape new user
            else:
                return

        # If the file does not exist...
        else:
            print("Creating a new file.")
            print("\nThis is the path: " + str(path))
            print("Retreiving Tweets from @" + str(username) + "...\n")

            # Iterating through user' tweets (REST)
            for status in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items():
                # Unfortunately, we have to set ensure_ascii to False because it does 
                # not encode Emojis properly--which is a problem when comparing strings.
                try:
                    self.print_tweet(status)
                    tweets.append(status._json)
                    tweet_count += 1

                except StopIteration:
                    break

            # Write to path.
            self.write(path, tweets)
            del tweets
            print("\n\n✧･ﾟAmount of Tweets Scraped: " + str(tweet_count) + " ･ﾟ･✧\n")

    def scrape(self, api):
        iter_check = True

        # Keep doing it until we want to do it.
        while iter_check:
            username = self.getUser(api).screen_name
            self.extract(api, username)               # Extract wanted info.
            usr_input = "abc"

            # Check if we want to scrape again.
            while True:
                try:
                    usr_input = str(input("\nWould you like to scrape again? (yes): "))
                    if usr_input in self.VALID:
                        break
                except ValueError:
                    print("\nThat was an invalid input. Proper responses: '', 'y', 'n', 'yes', 'no'\n")

                # Scrape again!
                if usr_input in self.YES:
                    os.system('cls||clear')
                    continue

                # Stop scraping!
                elif usr_input in self.NO:
                    iter_check = False
                    break

                # Errored out.
                else:
                    raise RuntimeError("Should not be possible. Breaking")
