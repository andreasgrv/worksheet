#!/usr/bin/python3
import argparse
import re
import random
from textblob import TextBlob
from collections import defaultdict


class Corpus(object):

    """A text representation created from smaller files """

    def __init__(self, filenames):
        """Create a corpus from the files"""
        self.filenames = filenames
        self.texts = {}
        for filename in filenames:
            with open(filename, 'r') as f:
                self.texts[filename] = f.read()

    @property
    def text(self):
        """Add text as attribute to corpus without
        saving the text a second time if it isn't used
        :returns: The text of all the corpus

        """
        # TODO: maybe move out this regex sub to somewhere else
        return re.sub(r'\s+', ' ', ' '.join(self.texts.values()))

    def locate_sentences(self, words, maxlen=125, minlen=25, shuffle=True):
        """ Sentence locator for words

        :words: The words
        :returns: A dictionary mapping a word to the sentences
                  it was found in

        """
        mapping = defaultdict(list)
        blob = TextBlob(self.text)
        for sentence in blob.sentences:
            if minlen < len(sentence) < maxlen:
                for word in sentence.tokens:
                    if word in words:
                        mapping[word].append(sentence.raw)
        if shuffle:
            for words in mapping.values():
                random.shuffle(words)
        return mapping

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create an exercise')
    parser.add_argument('-t', '--type', type=str, dest='type',
                        help='The type of exercise to create: eg: omit')
    parser.add_argument('-i', '--input', type=str, nargs='+', dest='files',
                        help=('The files to get text from'
                              ' to create the exercises'))
    parser.add_argument('-w', '--words', type=str, nargs='+', dest='words',
                        help=('The words to omit from sentences'
                              ' when creating the exercises'))
    args = parser.parse_args()
    ex_type = args.type
    files = args.files
    words = args.words

    # combine texts to one
    corpus = Corpus(files)
    found = corpus.locate_sentences(words)
    for word, sentences in found.items():
        for sent in sentences:
            replacement = r'\enskip\rule{%smm}{0.2mm}\enskip'
            print('%s\n' % sent.replace(word, replacement % (len(word)*3)))

    # case for omit type of exercise
