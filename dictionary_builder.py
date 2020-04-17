#!/usr/bin/env python3
import queries
import connection_handler

from IPython import embed
import mysql.connector


class Dictionary_Builder:
    def __init__(self, object_values):
        self.object_values = object_values
        self.build_dictionary()
        self.get_unknowns()

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
