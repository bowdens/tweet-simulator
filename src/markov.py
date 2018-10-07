from src.graph import Graph
import random

class Markov(object):
    def __init__(self):
        self.__graph = Graph()

    @property
    def graph(self):
        return self.__graph

    # add all the words in the list to the graph
    def add_words(self, words):
        # make sure words is a list
        if not isinstance(sentence, list):
            raise TypeError("Words must be a list")

        if len(words) == 0:
            return

        # add the first word in the list
        if not isinstance(word, str):
            raise TypeError("All words must be a string")
        if not self.graph.is_vertex(words[0]):
            self.graph.add_vertex(words[0])


        # from the 2nd word in the list to the last, add each and increment the edge
        for i in range(1, len(words)):
            if not isinstance(word, str):
                # make sure each element is a string
                raise TypeError("All words must be a string")

            if not self.graph.is_vertex(words[i]):
                # add the word as a node in the graph if it doesn't already exist
                self.graph.add_vertex(words[i])

            # increment the edge from the previous word to the current word
            self.graph.increment_edge(words[i-1], words[i])

    def get_next_word(self, word):
        if not self.graph.is_vertex(word):
            string = "\"" + word + "\": "
            for letter in word:
                string += str(ord(letter)) + " "
            raise ValueError("That word is has not been seen before (\"{}\")".format(string))

        total = 0
        for v in self.graph.verticies:
            total += self.graph.get_edge(word, v)

        rand = random.randint(0, total-1)
        count = 0
        for v in self.graph.verticies:
            count += self.graph.get_edge(word, v)
            if rand < count:
                return v

    def create_sentence(self):
        sentence = ""
        word = "\2"
        while True:
            if word != "\2" and word != "\3":
                sentence += " "
            word = self.get_next_word(word)
            if word == "\3":
                break
            sentence += word
        return sentence
