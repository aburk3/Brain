#!/usr/bin/env python3
import connection_handler
from queries import queries

from IPython import embed
import mysql.connector

from managers.word_manager import Word_Manager
from managers.phrase_manager import Phrase_Manager
from models.person import Person
from utils.dictionary_builder import Dictionary_Builder

from utils import custom_logging


class Person_Manager:
    def __init__(self):
        print("--Person Initializer")
        self.LOGGER = custom_logging.setup_custom_logger("Person Manager")

    def get_name(self):
        print("--Getting user name!--")
        user_input = input(f"Who is this? ")
        user_input_lower = user_input.lower()
        person = user_input_lower.split()
        return person

    def check_for_person(self):
        print("--Check_for_person()--")
        person = self.get_name()
        self.determine_name_format(person)

    def determine_name_format(self, person):
        print("--Determining name format!--")
        if len(person) == 1:
            self.name_status = 'FIRST'
            if self.check_for_first(person) == False:
                self.get_full_name()
        elif len(person) == 2:
            self.name_status = 'FIRST_LAST'
            self.check_exists_or_create(person)
        elif len(person) == 3:
            self.name_status == 'FULL'
        elif len(person) == 0:
            print("Call to check_for_person - 1")
            self.check_for_person()

        self.person_name = person

    def check_exists_or_create(self, person):
        print("--Checking if person exists, or creating!--")
        self.establish_new_connection()
        try:
            self.cursor.execute(queries.check_for_person(person[0], person[1]))
        except Exception as e:
            print("Exception has occured 50: " + str(e))
        result = self.cursor.fetchall()
        list_result = [list(i) for i in result]
        if len(list_result) > 0:
            print("Person was found!")
            person = list_result[0]
            self.create_person(person)
        else:
            print("Person not found, will create a new person")
            self.new_person(person)

    def check_last_interaction(self):
        self.establish_new_connection()

        self.LOGGER.info(f'Executing query to retrieve latest interaction')
        self.cursor.execute(queries.last_interaction())

        try:
            result = self.cursor.fetchall()
        except Exception as e:
            print("Exception has occured 50: " + str(e))
            self.LOGGER.debug(f'Failed to execute/fetchall from query: {e}')

        list_result = [list(i) for i in result]
        person = list_result[0]
        self.LOGGER.info(f'Last interaction values: {person}')

        return person

    def create_person(self, person):
        self.person = self.create_person_dict(person)
        print("--Instantiating new person--")
        self.update_latest_interaction(self.person)
        self.refresh_person()

    def update_person(self, person_id, attribute_to_update, value):
        print("--Updating person--")
        self.establish_new_connection()

        try:
            self.cursor.execute(queries.update_object(
                'persons', person_id, attribute_to_update, value))
        except Exception as e:
            print("Exception has occured 132: " + str(e))

        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

    def create_person_dict(self, person):
        print("--Creating person dict--")
        dictionary_builder = Dictionary_Builder(person)
        dictionary_builder.determine_object_type()
        dictionary_builder.get_object_attributes()
        dictionary_builder.build_dictionary()

        return dictionary_builder.dictionary

    def refresh_person(self):
        print("--Refreshing person--")
        self.establish_new_connection()
        try:
            self.cursor.execute(queries.person_by_id(self.person['id']))
        except Exception as e:
            print("Exception has occured 50: " + str(e))
        result = self.cursor.fetchall()
        list_result = [list(i) for i in result]

        person = list_result[0]
        self.create_person_dict(person)

    def check_for_first(self, person):
        print("--Checking for first_name--")
        self.first_name = person[0].strip()

        self.establish_new_connection()
        try:
            self.cursor.execute(queries.check_for_person_first(
                self.first_name))
        except Exception as e:
            print("Exception has occured 99: " + str(e))

        result = self.cursor.fetchall()
        person_to_check = 0
        list_result = [list(i) for i in result]

        if self.check_exists_result(list_result):
            person = list_result[0]
            person_dictionary = self.create_person_dict(person)
            self.person = Person(person_dictionary)

            user_input = input(
                f"Oh is this {self.person.first_name} {self.person.last_name}? ")
            word_or_phrase = user_input.split()[0]
            if Word_Manager.is_confirmation(word_or_phrase) or Phrase_Manager.is_confirmation(word_or_phrase):

                self.update_latest_interaction(self.person)
            else:
                return False
        else:
            return False

    def new_person(self, person):
        print("--Creating a new person--")

        self.establish_new_connection()

        try:
            self.cursor.execute(queries.create_person(
                person[0], person[1]))
        except Exception as e:
            print("Exception has occured 132: " + str(e))

        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

        self.assign_person(person)

    def update_latest_interaction(self, person):
        print("--Updating latest interaction--")
        self.establish_new_connection()
        value_string = ""
        word_id = person['id']
        for key, val in person:
            value_string = value_string + str(val)
        try:
            self.cursor.execute(
                queries.update_interaction(word_id, value_string))
        except Exception as e:
            print("Exception has occured 146: " + str(e))

        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

    def get_full_name(self):
        print("--Get user full name--")
        user_input = input(
            f"What is your full name? ")
        person = user_input.split()
        self.determine_name_format(person)

    def assign_person(self, person):
        print("--Assigning person--")
        self.establish_new_connection()
        try:
            self.cursor.execute(queries.check_for_person(person[0], person[1]))
        except Exception as e:
            print("Exception has occured 50: " + str(e))
        result = self.cursor.fetchall()
        list_result = [list(i) for i in result]

        person = list_result[0]
        self.create_person(person)

    def check_exists_result(self, result):
        result_list = [list(i) for i in result]

        if len(result_list) > 0:
            return True
        else:
            return False

    def establish_new_connection(self):
        self.LOGGER.info(f'Attempting to establish a new connection')
        try:
            connection = connection_handler.establish_connection()
            self.cnx = connection[0]
            self.cursor = connection[1]
        except Exception as e:
            self.LOGGER.debug(f'Failed to establish connection: {e}')

    def compare_person(self, last_interaction_person, given_name):
        last_interaction_first_n = last_interaction_person['first_name']
        last_interaction_last_n = last_interaction_person['last_name']


        # We need to find out if the 'given name' is first and last
        # or only first (deal with only last in future maybe)
        if len(given_name) == 1:
            first_name_given = given_name[0]

            return self.check_for_match_first(first_name_given, last_interaction_first_n)
        elif len(given_name) == 2:
            first_name_given = given_name[0]
            last_name_given = given_name[1]

            return self.check_for_match_first_last(first_name_given, last_name_given, last_interaction_first_n, last_interaction_last_n)

    def check_for_match_first(self, first_name_given, last_interaction_first_n):
        if first_name_given == last_interaction_first_n:
            return True
        else:
            return False

    def check_for_match_first_last(self, first_name_given, last_name_given, last_interaction_first_n, last_interaction_last_n):
        if (first_name_given == last_interaction_first_n and last_name_given == last_interaction_last_n):
            return True
        else:
            return False


    @staticmethod
    def update_latest_interaction_s(person):
        connection = connection_handler.establish_connection()
        cnx = connection[0]
        cursor = connection[1]
        try:
            cursor.execute(queries.update_interaction(
                person.first_name, person.last_name))
        except Exception as e:
            print("Exception has occured 212: " + str(e))

        cnx.commit()
        cursor.close()
        cnx.close()
