# twitter_json.py -*- formatting jsons -*-
#
# Author:  Daniel Choo
# Date:    11/22/19
# URL:     https://
# License: MIT

import tweepy


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
        compressed, yet information-heavy JSON.
    """
    def __init__(self):
        """ __init__(tweet):  Constructor; nothing needs to be initialized though.
            Returns:          N/A [Nothing]
        """
        pass

    def tweet(self, tweet):
        """ tweet():          Encodes tweets (object: Status) into truncated
                              key-pair values.
            Returns:          tweet [Dict (multiple data types)]
        """
        tweet = {
               'created_at': None,
               'id_str': None,
               'text': None,
               'user': {
                   'id': None,
                   'name': None,
                   'screen_name': None,
                   'url': None,
                   'description': None,
               },
               'place': {},
               'entities': {
                    'hashtags': [],
                    'urls': [],
                    'user_mentions': [],
               },
        }
        return tweet

    def retweet(self, tweet):
        """ retweet(tweet):   Encodes retweets into dictionaries.
            Returns:          retweet [Dict (multiple data types)]
        """
        retweet = {
            'created_at': None,
            'id': None,
            'id_str': None,
            'text': None,
            'truncated': None,
            'text_range': None,
            'entities': {
                'hashtags': [],
                'urls': [],
                'user_mentions': [],
            }

        }
        return retweet

    def extended(self, tweet):
        """ extended(tweet):  Encodes extended tweets into dictionaries.
            Returns:          extended [Dict (multiple data types)]
        """
        extended = {
        }
        return extended

    def quote(self, tweet):
        """ quote(tweet):    Encodes extended tweets into dictionaries.
            Returns:          quotes [Dict (multiple data types)]
        """
        quote = {
        }
        return quote
