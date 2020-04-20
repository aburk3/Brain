#!/usr/bin/env python3
import queries
import connection_handler

from IPython import embed
import mysql.connector

import logging


class Dictionary_Builder:
    def __init__(self, object_values):
        self.object_values = object_values
        # self.build_dictionary()
        # self.get_unknowns()

    def get_object_attributes(self):
        object_id = self.object_values[7]
        self.establish_new_connection()

        logging.info(f'Executing query to retrieve object attributes.')
        self.cursor.execute(queries.get_object_attributes())

        try:
            result = self.cursor.fetchall()
        except Exception as e:
            print("Exception has occured 50: " + str(e))
            logging.debug(f'Failed to execute/fetchall from query: {e}')

        list_result = [list(i) for i in result]
        person = list_result[0]
        logging.info(f'Last interaction: {person}')

    def build_dictionary(self):
        attributes = self.object_values[-1].split(',')
        self.dictionary = {}
        values = self.object_values[3].split(',')
        for index, attribute in enumerate(attributes):
            self.dictionary[attribute] = values[index]

    def get_unknowns(self):
        new_list = [k for k, v in self.dictionary.items(
        ) if v == '' and k != 'count' and k != 'created']
        self.dictionary["unknowns"] = new_list

    def establish_new_connection(self):
        logging.info(f'Attempting to establish a new connection')
        try:
            connection = connection_handler.establish_connection()
            self.cnx = connection[0]
            self.cursor = connection[1]
        except Exception as e:
            logging.debug(f'Failed to establish connection: {e}')
