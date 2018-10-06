from src.graph import Graph
import random

class Markov(object):
    def __init__(self):
        self.__graph = Graph()

    @property
    def graph(self):
        return self.__graph

    def add_sentence(self, sentence):
        if not isinstance(sentence, str):
            raise TypeError("Setence must be a string")

        words = []
        tmp_words = sentence.split()
        tmp_words.insert(0, "\2")
        tmp_words.append("\3")
        for word in tmp_words:
            if word[0] == '@':
                words.append(word[1:])
                if not self.graph.is_vertex(word[1:]):
                    self.graph.add_vertex(word[1:])
            elif "twitter.com" in word:
                continue
            else:
                if not self.graph.is_vertex(word):
                    self.graph.add_vertex(word)
                words.append(word)


        for i in range(0, len(words)-1):
            self.graph.increment_edge(words[i], words[i+1])

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
