#!/usr/bin/env python3
import connection_handler
# from word_manager import Word_Manager
from managers.phrase_manager import Phrase_Manager
from managers.person_manager import Person_Manager
from managers import chat_manager
from queries import queries
from utils import custom_logging

from IPython import embed
import mysql.connector
import sys
import os
import logging

from dotenv import load_dotenv
load_dotenv()


class Brain_Manager:
    def __init__(self):
        self.USER = os.getenv("USER")
        self.PASSWORD = os.getenv("PASSWORD")
        self.LOGGER = custom_logging.setup_custom_logger("Manager")

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

    def determine_person(self, person_manager):
        # First, find out who is speaking
        given_name = chat_manager.ask_who()

        # Find out last interaction, to guess who is speaking
        # Especially useful if only first name is given
        last_interaction = person_manager.check_last_interaction()

        # Compare last ineraction with given name
        last_interaction_person = person_manager.create_person_dict(last_interaction)

        # Find out if what was given could be matched with the last interaction
        match_result = person_manager.compare_person(last_interaction_person, given_name)

        # Determine if first name or first and last name were given
        first_or_first_last = self.determine_first_or_first_last(given_name)

        if first_or_first_last == 'first':
            chat_manager.get_first_last_confirmation(last_interaction_person)
        else:
            print("Person confirmed!")

    def determine_first_or_first_last(self, given_name):
        if len(given_name) == 1:
            return 'first'
        else:
            return 'first_last'


if __name__ == '__main__':
    brain = Brain_Manager()
    person_manager = Person_Manager()

    person = brain.determine_person(person_manager)




