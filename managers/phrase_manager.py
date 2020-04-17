#!/usr/bin/env python3
import queries
import connection_handler

from IPython import embed
import mysql.connector

import grammar_format

from dotenv import load_dotenv
from managers.word_manager import Word_Manager

import re
load_dotenv()


class Phrase_Manager:
    def __init__(self, phrase="None", person="None", person_manager="None"):
        self.person = person
        self.person_manager = person_manager
        lower_phrase = phrase.lower()
        result = lower_phrase.find("?")
        self.new_phrase = self.remove_bad_chars(lower_phrase)
        self.parsed_phrase = self.new_phrase.split()
        # self.determine_if_possessive()
        # self.save_new_phrase(phrase)
        # self.check_for_assigning_attribute()

        if lower_phrase == 'teach':
            self.teach_phrase()
        else:
            if result == -1:
                print("That is a statement")
            else:
                self.get_question_format()

    def get_question_format(self):
        question_format = ''

        for word in self.parsed_phrase:
            word_manager = Word_Manager(word)
            question_format += grammar_format.assign_part_of_speech(
                word_manager.word)

        embed()

    def check_for_assigning_attribute(self):
        if self.possessive and self.check_for_attribute():
            self.assign_attribute()

    def check_for_attribute(self):
        attribute_reference = self.parsed_phrase.index("is")
        attribute_index = attribute_reference - 1
        self.attribute = self.parsed_phrase[attribute_index]
        if self.attribute == 'name':
            try:
                first_or_last = self.parsed_phrase[attribute_index - 1]
                self.attribute = first_or_last + "_" + self.attribute
            except Exception as e:
                print("Exception has occured 48: " + str(e))
        self.get_new_value()
        if hasattr(self.person, self.attribute):
            return True
        else:
            return False

    def get_new_value(self):
        self.new_value_index = self.parsed_phrase.index("is") + 1
        self.new_value = self.parsed_phrase[self.new_value_index]
        if self.attribute == 'first_name' or self.attribute == 'last_name':
            self.new_value = self.new_value.capitalize()

    def assign_attribute(self):
        self.person_manager.update_person(
            self.person.id, self.attribute, self.new_value)
        print("Updated!")

    def determine_if_possessive(self):
        self.establish_new_connection()
        word = self.parsed_phrase[0]
        try:
            self.cursor.execute(queries.check_possessive(word))
        except Exception as e:
            print("Exception has occured 40: " + str(e))

        result = self.cursor.fetchall()

        self.list_result = [list(i) for i in result]
        if 'is' in self.parsed_phrase:
            if self.check_exists_result(self.list_result):
                self.possessive = True
        else:
            self.possessive = False

    # def handle_question(self):
    #     phrases = self.get_questions()

    def get_questions(self):
        self.establish_new_connection()

        try:
            self.cursor.execute(queries.get_questions())
        except Exception as e:
            print("Exception has occured 40: " + str(e))

        result = self.cursor.fetchall()

        self.list_result = [list(i) for i in result]
        print("Results: " + str(self.list_result))

    def save_new_phrase(self, phrase):
        self.establish_new_connection()
        try:
            self.cursor.execute(queries.save_new_phrase(
                phrase, self.person.id))
            phrase_id = self.cursor.lastrowid
        except Exception as e:
            print("Exception has occured 54: " + str(e))
        self.cnx.commit()

        try:
            self.cursor.execute(queries.save_person_phrase_matrix(
                phrase_id, self.person.id))
        except Exception as e:
            print("Exception has occured 61: " + str(e))
        self.cnx.commit()

        self.cursor.close()
        self.cnx.close()

    def remove_bad_chars(self, phrase):
        bad_chars = [';', ':', '!', "*", "?"]
        for i in bad_chars:
            phrase = phrase.replace(i, '')

        return phrase

    def teach_phrase(self):
        self.phrase = input(
            f"What new phrase would you like to teach me?")

        if self.check_if_known():
            print(f"I already know the phrase {self.phrase}")
        else:
            self.learn_phrase()

    def learn_phrase(self):
        self.definition = input(
            f"What does the phrase {self.phrase} mean? ")
        print("Thanks! I'll remember that.")
        self.save_new_phrase()

    def learn_phrase(self, phrase):
        print(f"I'm now learning the phrase: {phrase}")

    def check_if_known(self):
        if self.check_for_phrase():
            self.phrase_known()
        else:
            self.phrase_not_known()

    def check_for_phrase(self):
        try:
            self.cursor.execute(queries.check_for_phrase(self.phrase))
        except Exception as e:
            print("Exception has occured 102: " + str(e))
        result = self.cursor.fetchall()
        self.check_exists_result(result)

    def check_exists_result(self, result):
        result_list = [list(i) for i in result]
        number_returned = result_list[0][0]
        if int(number_returned) > 0:
            return True
            self.update_phrase()
        else:
            return False

    def update_phrase(self):
        try:
            self.cursor.execute(queries.update_phrase(
                phrase, self.person.person_id))
        except Exception as e:
            print("Exception has occured: 120 " + str(e))
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

    def establish_new_connection(self):
        connection = connection_handler.establish_connection()
        self.cnx = connection[0]
        self.cursor = connection[1]

    @staticmethod
    def is_confirmation(word_or_phrase):
        Phrase_Manager.establish_new_connection()

        try:
            cursor.execute(queries.check_for_confirmation(word_or_phrase))
        except Exception as e:
            print("Exception has occured 144: " + str(e))
        result = cursor.fetchall()

        if Phrase_Manager.confirmation_exists(result):
            return True
        else:
            return False

    @staticmethod
    def confirmation_exists(result):
        result_list = [list(i) for i in result]
        number_returned = result_list[0][0]
        if int(number_returned) > 0:
            return True
        else:
            return False
