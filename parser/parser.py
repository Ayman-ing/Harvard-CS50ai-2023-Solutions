from lib2to3.pgen2.tokenize import tokenize

import nltk

nltk.download('punkt_tab')

import sys



TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP | NP VP Conj NP VP
NP -> N | Det N | P N |  Det Adj N| Det Adj Adj Adj N P Det N  P Det N  | Det Adj Adj N P N | Det Adj N P N | N P Det Adj N | Det N P N | P Det Adj N | N Adv | P Det N Adv | Adv 
VP -> V | V NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    l =nltk.word_tokenize(sentence)
    returned_list=[]
    for ch in l:
        if  ch.isalpha():
            returned_list.append(ch.lower())
    return returned_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrase_chunks = []

    # Iterate over all NP subtrees
    noun_phrase_chunks = []

    for subtree in tree.subtrees(lambda t: t.label() == "NP" and not any(t.subtrees(lambda tt: tt.label() == "NP" and tt!=t))):
        noun_phrase_chunks.append(subtree)

    return noun_phrase_chunks


if __name__ == "__main__":
    main()
