#!/usr/bin/env python3
from queries import queries
import connection_handler

from IPython import embed
import mysql.connector

from utils import custom_logging


class Dictionary_Builder:
    def __init__(self, object_values):
        self.object_values = object_values
        self.LOGGER = custom_logging.setup_custom_logger("Dictionary Builder")
        self.LOGGER.info(f'Executing query to retrieve object attributes.')

    def determine_object_type(self):
        self.object_type = self.object_values[7]

    def get_object_attributes(self):
        self.establish_new_connection()

        self.LOGGER.info(f'Executing query to retrieve object attributes.')
        self.cursor.execute(queries.get_object_attributes(self.object_type))

        try:
            result = self.cursor.fetchall()
        except Exception as e:
            self.LOGGER.debug(f'Failed to execute/fetchall from query: {e}')

        list_result = [list(i) for i in result]
        self.attributes = list_result[0][0].split(',')
        self.LOGGER.info(f'Object attributes: {self.attributes}')

    def build_dictionary(self):
        values = self.object_values[-1].split(',')
        self.dictionary = {}
        for index, attribute in enumerate(self.attributes):
            self.dictionary[attribute] = values[index]
        embed()

    def get_unknowns(self):
        new_list = [k for k, v in self.dictionary.items(
        ) if v == '' and k != 'count' and k != 'created']
        self.dictionary["unknowns"] = new_list

    def establish_new_connection(self):
        self.LOGGER.info(f'Attempting to establish a new connection')
        try:
            connection = connection_handler.establish_connection()
            self.cnx = connection[0]
            self.cursor = connection[1]
        except Exception as e:
            self.LOGGER.debug(f'Failed to establish connection: {e}')
