# twitter_json.py -*- formatting jsons -*-
#
# Author:  Daniel Choo
# Date:    11/22/19
# URL:     https://www.github.com/kyoogoo/twump
# License: MIT

import os
import tweepy
import json


class Encode:
    """ Encode() aims to encode the tweepy.models.Status object back into
        a dictionary that can be converted into a JSON. Unfortuntely, as
        mentioned in the source code of extract.py, but JSONParser() does not
        function properly, this has been a bug for a while now. Also, it is not
        possible to hard cast a class into a dictionary. Also, I could simply
        just create a new dictionary and append in each single key-pair value,
        but there are just simply too many; as there were a lot of extraneous
        variables that I deepemed pretty unnecessary--e.g., repeating vars,
        repeating information, or simply random information that just takes up
        space (one tweet can take up to 24KB!) So, I have created this to
        circumvent the problem--creating my own parser.

        Thus, reiterating the previous paragraph, I have created this parser to
        truncate some variables Twitter provides and try to create a more
        compressed, yet information-heavy JSON. Fundamentally, this parser will
        detect the type of Tweet (tweet, retweet, extended, or quote), parse
        the Status object and covert it into a dictionary accordingly, and
        return the dictionary back to the program/user.

        According to Twitter's documentation, a tweet's JSON is configured
        in this format (https://developer.twitter.com/en/docs/tweets/data-
        dictionary/overview/intro-to-tweet-json#retweet):

        - Tweet (a Status object): the root of the JSON
            + User: Account data.
            + Entities: Includes URLS (https://twitter.com), Hashtags
                        (#trashtag), Mentions (@adriyens), and Symbols ($)
            x Extended Entities (Omitted from this parser. Too much data.)
            x Places (Omitted from this parser. Although would be interesting.)
    """
    def __init__(self):
        """ __init__(self):  Constructor; nothing needs to be initialized though.
            Returns:          N/A [Nothing]
        """
        pass

    def encode(self, status, t_type):
        """ encode(status, t_type): Encodes the object into an JSON-appropriate
                                    dictionary.
            Returns:                N/A [Nothing]
        """
        try:
            if t_type == "tweet":
                tweet = tweet()
            elif t_type == "retweet":
                tweet = retweet()
            elif t_type == "quote":
                tweet = quote()
            elif t_type == "extended":
                tweet = extended()
        except :
	        



        for key in status.items():
            if key == 'user':
                temp = users(key)
                tweet[key] = temp
            elif key == 'entities':
                temp = entities(key)
                tweet[key] = temp
                
    def tweet(self):
        """ tweet(status): Encodes tweets (Status) into a dictionary.
            Returns:       tweet (Dict)
        """
        tweet = {
            'created_at': None,
            'id_str':     None,
            'text':       None,
            'user': {
                'id':          None,
                'name':        None,
                'screen_name': None,
                'description': None,
                'url':         None,
            },
            'place': {},
            'coordinates': None,
            'place': None,
            'retweet_count': None,
            'favorite_count': None,
            'lang': None
        },
        return tweet

    def user(self, username):
        """ user(self, entity): Read in all the entities.
            Return:                 entities (dict)
        """
        pass

    def entities(self, entity):
        """ entities(self, entity): Read in all the entities.
            Return:                 entities (dict)
        """

        entities = {},

        for key, val in entity.items():
            entities[key] = val

        return entities

    def retweet(self):
        """ retweet(tweet):   Returns retweets (Status) in dict format.
            Returns:          retweet (Dict)
        """
        retweet = {
            'created_at': None,
            'id_str':     None,
            'text':       None,
            'truncated':  None,
            'text_range': None,
            'entities': {
                'hashtags':      [],
                'urls':          [],
                'user_mentions': [],
            },
            'user': {
                'id':              None,
                'id_str':          None,
                'name':            None,
                'screen_name':     None,
                'location':        None,
                'followers_count': None,
                'friends_count':   None,
                'verified':        None,
            },
            'retweeted_status': {
                'created_at':         None,
                'id':                 None,
                'id_str':             None,
                'full_text':          None,
                'truncated':          None,
                'display_text_range': [],
                'entities': {
                    'hashtags':      [],
                    'symbols':       [],
                    'user_mentions': [],
                },
                'user': {
                    'id':             None,
                    'id_str':         None,
                    'name':           None,
                    'screen_name':    None,
                    'location':       None,
                    'follower_count': None,
                    'friends_count':  None,
                    'verified':       None,
                },
                'is_quote':      None,
                'retweet_count': None,
            },
        },

        # Where the fun begins.

        return retweet

    def extended(self):
        """ extended(tweet):  Returns extended (Status) in dict format.
            Returns:          extended (Dict)
        """
        extended = {
            'created_at': None,
            'id_str':     None,
            'text':       None,
            'truncated':  None,
            'text_range': None,
        },

       return extended

    def quote(self):
        """ quote(tweet):    Returns extended (Status) in dict format.
            Returns:         quotes (Dict)
        """
        quote = {
            "text": None,
            "user": {
                "screen_name": None,
            },
            "quoted_status": {
                "text": None,
                "user": {
                    "screen_name": None,
                },
	            "place": {},
	            "entities": {},
	            "extended_entities": {}
            },  
	        "quoted_status_permalink": {
		        "url": None,
		        "expanded": None,
		        "display": None,
	        },    
	        "place": {},
	        "entities": {
		        "urls": []
	        }
        },

        return quote
