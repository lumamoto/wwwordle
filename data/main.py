from collections import OrderedDict
from dotenv import load_dotenv
import lyricsgenius as lg
import random
import os
# import nltk
# import ssl
# try: _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError: pass
# else: ssl._create_default_https_context = _create_unverified_https_context
# nltk.download("stopwords")
from nltk.corpus import stopwords

load_dotenv()
GENIUS_ACCESS_TOKEN = os.environ["GENIUS_ACCESS_TOKEN"]

MIN_WORD_LENGTH = 5
MAX_WORD_LENGTH = 10

def get_lyrics(artists):
    """
    Retrieves all lyrics from a given list of artists and stores them in raw.txt.

    Args:
        artists (list): List of artists to pull lyrics from.
    """
    genius = lg.Genius(
        GENIUS_ACCESS_TOKEN,
        skip_non_songs=True,
        remove_section_headers=True,
        excluded_terms=["(Remastered)"]
    )
    raw_text = open("raw.txt", "w")
    for artist in artists:
        songs = genius.search_artist(artist).songs
        s = [song.lyrics.lower() for song in songs]
        raw_text.write("\n\n".join(s))
    raw_text.close()

def clean_text():
    """
    Cleans the text in raw.txt and stores it in clean.txt.
    """
    raw_text = open("raw.txt", "r")
    sw_set = set(stopwords.words("english"))
    text_set = set(raw_text.read().split()) # Unique words
    text_set = text_set.difference(sw_set)

    clean_set = set()
    for word in text_set:
        word = word.replace("embed", "")
        word = word.replace("lyrics", "")
        word = word.replace("\u0435", "e") # Special character
        if word.isalpha() and word != "thats": # Ignore words with punctuation and "thats"
            clean_set.add(word)
    
    clean_text = open("clean.txt", "w")
    for word in clean_set:
        clean_text.write(f"{word} ")
    raw_text.close()
    clean_text.close()

def create_dict():
    """
    Creates an Ordered Dictionary from words in clean.txt of lengths and
        their words.

    Returns:
        OrderedDict: Ordered Dictionary where the key is the length
            of a word and the value is a list containing all words of
            that length.
    """
    word_dict = OrderedDict()
    clean_text = open("clean.txt", "r")
    text_list = clean_text.read().split()
    for word in text_list:
        if len(word) not in word_dict:
            word_dict[len(word)] = [word]
        else:
            word_dict[len(word)].append(word)
    word_dict = sorted(word_dict.items())
    dict_text = open("dict.txt", "w")
    for (word_length, words) in word_dict:
        if MIN_WORD_LENGTH <= word_length <= MAX_WORD_LENGTH:
            dict_text.write(f"Length: {word_length}\n{words}\n\n")
            print(f"{len(words)} {word_length}-letter words")
    clean_text.close()
    dict_text.close()
    return word_dict

def create_wordlist(words):
    """
    Creates wordlist.ts from a given list of words.

    Args:
        words (list): List of words to be in wordlist.ts.
    """
    wordlist_ts = open("../src/constants/wordlist.ts", "w")
    wordlist_ts.write(f"export const WORDS = {words}")
    wordlist_ts.close()

def create_validGuesses(words):
    """
    Creates validGuesses.ts by combining known valid words and a list of
        given words.

    Args:
        words (list): List of (Will Wood) words to union with already 
            known valid words.
    """
    with open("givenValidWords.txt") as f:
        valid_list = f.read().splitlines()
    validGuesses_list = list(set(words) | set(valid_list))
    validGuesses_ts = open("../src/constants/validGuesses.ts", "w")
    validGuesses_ts.write(f"export const VALID_GUESSES = {validGuesses_list}")
    validGuesses_ts.close()

def main():
    artists = ["Will Wood", "Will Wood and the Tapeworms"]
    # get_lyrics(artists)
    clean_text()
    word_dict = create_dict()
    words = word_dict[MIN_WORD_LENGTH-1][1]
    random.shuffle(words)
    create_wordlist(words)
    create_validGuesses(words)

main()