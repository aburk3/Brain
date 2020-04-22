#!/usr/bin/env python3
from managers.word_manager import Word_Manager

def ask_who():
    user_input = input(f"Who is this? ")
    user_input_lower = user_input.lower()
    given_name = user_input_lower.split()
    return given_name

def get_first_last_confirmation(last_interaction_person):
    word_manager = Word_Manager()

    user_input = input(f"Is this {last_interaction_person['first_name']} {last_interaction_person['last_name']}")
    if word_manager.is_confirmation(user_input):
        return True
    else:
        return False
