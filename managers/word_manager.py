#!/usr/bin/env python3
import queries
import connection_handler

from IPython import embed
import mysql.connector
from PyDictionary import PyDictionary
from utils.dictionary_builder import Dictionary_Builder
from models.word import Word


class Word_Manager:
    def __init__(self):
        self.dictionary = PyDictionary()

    def teach_word(self):
        user_input = input(
            f"What new word would you like to teach me?")
        words = user_input.split()

        self.word = words[0]

        if self.check_if_known():
            print(f"I already know the word {self.word}")
        else:
            self.learn_word()

    def learn_word(self):
        self.definition = input(
            f"What does the word {self.word} mean? ")
        print("Thanks! I'll remember that.")
        self.save_new_word()

    def check_if_known(self):
        if self.check_for_word():
            return True
        else:
            return False

    def check_for_word(self):
        self.establish_new_connection()
        try:
            self.cursor.execute(queries.check_for_word(self.word))
        except Exception as e:
            print("Exception has occured 49: " + str(e))
        result = self.cursor.fetchall()
        if self.check_exists_result(result):
            return True
        else:
            return False

    def check_exists_result(self, result):
        result_list = [list(i) for i in result]
        number_returned = result_list[0][0]
        if int(number_returned) > 0:
            return True
        else:
            return False

    def save_new_word(self):
        try:
            self.cursor.execute(queries.save_new_word(
                self.word, self.definition))
        except Exception as e:
            print("Exception has 69: " + str(e))
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

    def establish_new_connection(self):
        connection = connection_handler.establish_connection()
        self.cnx = connection[0]
        self.cursor = connection[1]

    def is_confirmation(self, word_or_phrase):
        self.establish_new_connection()

        try:
            self.cursor.execute(queries.check_for_confirmation(word_or_phrase))
        except Exception as e:
            print("Exception has occured 93: " + str(e))
        result = self.cursor.fetchall()

        if self.confirmation_exists(result):
            return True
        else:
            return False

    def get_word(self, word):
        self.establish_new_connection()
        try:
            self.cursor.execute(queries.get_word(word))
        except Exception as e:
            print("Exception has occured 108: " + str(e))
        result = self.cursor.fetchall()
        list_result = [list(i) for i in result]

        word = list_result[0]
        self.create_word(word)
        return self.word

    def create_word(self, word):
        self.create_word_dict(word)
        print("--Instantiating new word--")
        self.word = Word(self.word_dict)

    def create_word_dict(self, word):
        print("--Creating word dict--")
        dictionary_builder = Dictionary_Builder('words', word)
        self.word_dict = dictionary_builder.dictionary

    @staticmethod
    def confirmation_exists(result):
        result_list = [list(i) for i in result]
        number_returned = result_list[0][0]
        if int(number_returned) > 0:
            return True
        else:
            return False
