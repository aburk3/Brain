#!/usr/bin/env python3
import connection_handler
import queries

from IPython import embed
import mysql.connector


from dotenv import load_dotenv
load_dotenv()


class Word:
    def __init__(self, dict):
        self.id = dict["id"]
        self.count = dict["count"]
        self.created = dict["created"]
        self.word = dict["word"]
        self.word_class = dict["word_class"]
        self.sub_class = dict["sub_class"]
        self.tense = dict["tense"]
        self.singular_plural = dict["singular_plural"]
        self.person = dict["person"]
        self.definition = dict["definition"]
        self.confirmation = dict["confirmation"]
