#!/usr/bin/env python3


def ask_who():
    user_input = input(f"Who is this? ")
    user_input_lower = user_input.lower()
    given_name = user_input_lower.split()
    return given_name


def ask_who():
    user_input = input(f"What is your full name? ")
    user_input_lower = user_input.lower()
    given_full_name = user_input_lower.split()
    return given_full_name
