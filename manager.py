#!/usr/bin/env python3
import connection_handler
# from word_manager import Word_Manager
from managers.phrase_manager import Phrase_Manager
from managers.person_manager import Person_Manager
from managers import chat_manager
from queries import queries

from IPython import embed
import mysql.connector
import sys
import os
import logging

from dotenv import load_dotenv
load_dotenv()


class Brain_Manager:
    def __init__(self):
        logging.basicConfig(filename='messages.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file.')
        self.USER = os.getenv("USER")
        self.PASSWORD = os.getenv("PASSWORD")

    def establish_new_connection(self):
        connection = connection_handler.establish_connection()
        self.cnx = connection[0]
        self.cursor = connection[1]

    def determine_response(self):
        if self.person_manager.person:
            self.handle_person_input()
        else:
            self.check_for_person()

    def check_for_person(self):
        print("--Finding out who I'm talking to--")
        self.person_manager = Person_Manager()

    def handle_person_input(self):
        self.talking_to = self.person_manager.person
        while len(self.person_manager.person['unknowns']) > 0:
            result = self.get_more_information()
            if result == False:
                break

        user_input = input(f"What's up? ")
        words = user_input.split()
        if words[0] == 'teach':
            if words[1] == 'word':
                vocab_manager = Word_Manager(words[0])
            elif words[1] == 'phrase':
                vocab_manager = Phrase_Manager(words[0])
        else:
            Phrase_Manager(user_input, self.person_manager.person,
                           self.person_manager)

    def get_more_information(self):
        first_unknown = self.person_manager.person['unknowns'][0]

        self.user_input = input(
            f"What is your {first_unknown}? Or type skip. ")
        if self.user_input != 'skip':
            self.person_manager.update_person(self.person_manager.person.id,
                                              first_unknown, self.user_input)
            self.state = 'learning'
            self.person_manager.refresh_person()
        else:
            return False

    def begin_program(self):
        self.cursor = connection_handler.establish_connection()
        self.get_user_input()


if __name__ == '__main__':
    brain = Brain_Manager()
    person_manager = Person_Manager()

    given_name = chat_manager.ask_who()
    person_last_interaction = person_manager.check_last_interaction()

    # full_name = chat_manager.ask_full_name()
