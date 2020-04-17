#!/usr/bin/env python3
import connection_handler
import queries

from IPython import embed
import mysql.connector


from dotenv import load_dotenv
load_dotenv()


class Person:
    def __init__(self, dict):
        self.id = dict["id"]
        self.first_name = dict["first_name"]
        self.last_name = dict["last_name"]
        self.address = dict["address"]
        self.phone = dict["phone"]
        self.occupation = dict["occupation"]
        self.marriage_status = dict["marriage_status"]
        self.sexual_orientation = dict["sexual_orientation"]
        self.sex = dict["sex"]
        self.age = dict["age"]
        self.birth_state = dict["birth_state"]
        self.allergies = dict["allergies"]
        self.hair_color = dict["hair_color"]
        self.eye_color = dict["eye_color"]
        self.count = dict["count"]
        self.created = dict["created"]
        self.frequency = dict["frequency"]
        self.unknowns = dict["unknowns"]
