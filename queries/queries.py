#!/usr/bin/env python3


def get_all():
    return """
		SELECT *
		FROM phrases;
	"""


def check_for_word(word):
    return f"""
		SELECT COUNT(*)
		FROM words
		WHERE word = '{word}';
	"""


def check_for_phrase(phrase):
    return f"""
		SELECT COUNT(*)
		FROM phrases
		WHERE phrase = '{phrase}';
	"""


def check_possessive(word):
    return f"""
        SELECT *
        FROM words
        WHERE word_class = 3
        AND sub_class = 6
        AND word = '{word}';
	"""


def save_new_word(word, definition):
    return f"""
		INSERT INTO words (word, definition)
		VALUES ('{word}', '{definition}');
	"""


def save_new_phrase(phrase, person_id):
    return f"""
		INSERT INTO phrases (phrase, person_id, frequency)
		VALUES ('{phrase}', {person_id}, 1);
	"""


def save_person_phrase_matrix(phrase_id, person_id):
    return f"""
		INSERT INTO person_phrase_matrix (phrase_id, person_id)
		VALUES ('{phrase_id}', {person_id});
	"""


def check_for_person(first_name, last_name):
    return f"""
            SELECT first_name.id, first_name.word, last_name.word, first_name.details, object.object, object.attributes
            FROM words AS first_name
            INNER JOIN words AS last_name
            ON first_name.id = last_name.word_id
            INNER JOIN objects AS object
            ON first_name.object_type = object.id
            WHERE first_name.word = '{first_name}'
            AND last_name.word = '{last_name}';
        """


# def check_for_person(first_name, last_name):
#     return f"""
#             SELECT *
#             FROM persons
#             WHERE first_name = '{first_name}'
#             AND last_name = '{last_name}';
#         """


def person_by_id(person_id):
    return f"""
            SELECT first_name.id, first_name.word, last_name.word, first_name.details, object.object, object.attributes
            FROM words AS first_name
            INNER JOIN words AS last_name
            ON first_name.id = last_name.word_id
            INNER JOIN objects AS object
            ON first_name.object_type = object.id
            WHERE first_name.id = {person_id};
        """


# def check_for_person_first(first_name):
#     return f"""
#             SELECT *
#             FROM persons
#             WHERE first_name = '{first_name}'
#             ORDER BY frequency DESC;
#         """
def check_for_person_first(first_name):
    return f"""
            SELECT first_name.id, first_name.word, last_name.word, first_name.details, object.object, object.attributes
            FROM words AS first_name
            INNER JOIN words AS last_name
            ON first_name.id = last_name.word_id
            INNER JOIN objects AS object
            ON first_name.object_type = object.id
            WHERE first_name.word = '{first_name}'
            LIMIT 1;
        """


def check_for_person_full(first_name, middle_name, last_name):
    return f"""
            SELECT *
            FROM persons
            WHERE first_name = '{first_name}'
            AND last_name = '{last_name}'
            AND middle_name = '{middle_name}';
        """


def check_for_confirmation(word):
    return f"""
        SELECT COUNT(*)
        FROM words
        WHERE word = '{word}'
        AND confirmation = 'TRUE';
    """


def update_interaction(word_id, value_string):
    return f"""
        UPDATE words
        SET last_interaction = NOW(),
        details = '{value_string}''
        WHERE id = '{word_id}';
    """


# def last_interaction():
#     return f"""
#         SELECT *
#         FROM words
#         WHERE sub_class = 13
#         ORDER BY last_interaction DESC
#         LIMIT 1;
#     """

def last_interaction():
    return f"""
        SELECT *
        FROM words
        WHERE sub_class = 13
        ORDER BY last_interaction DESC
        LIMIT 1;
    """


# def get_attributes(table):
#     return f"""
#         SELECT `COLUMN_NAME`
#         FROM `INFORMATION_SCHEMA`.`COLUMNS`
#         WHERE `TABLE_SCHEMA`='brain'
#             AND `TABLE_NAME`='{table}';
#     """

def get_object_attributes(object_id):
    return f"""
        SELECT attributes
        FROM objects
        WHERE object_id = object_id;
    """


def get_attributes(table):
    return f"""
        SELECT *
        FROM {table}
        LIMIT 1;
    """


def update_object(table, id_to_update, property_to_update, value):
    return f"""
        UPDATE {table}
        SET {property_to_update} = '{value}'
        WHERE id = {id_to_update};
    """


def get_person_attributes():
    return f"""
        SELECT *
        FROM phrases
        WHERE phrase_type = 'question'
        LIMIT 200;
    """


def create_person(first_name, last_name):
    return f"""
        INSERT INTO persons
        (
        first_name,
        last_name,
        last_interaction,
        frequency
        )
        VALUES
        (
            '{first_name}',
            '{last_name}',
            NOW(),
            1
        );
    """


def get_questions():
    return f"""
        SELECT *
        FROM phrases
        WHERE phrase_type = 'question'
        ORDER BY frequency DESC
        LIMIT 200;
    """


def update_phrase(phrase):
    return f"""
        UPDATE persons
        SET last_interaction = NOW(),
        frequency = frequency + 1
        WHERE phrase = '{phrase}';
    """


# def get_name():
#     return f"""
#         SELECT *
#         FROM phrases
#         WHERE phrase_type = ''
#         ORDER BY frequency DESC
#         LIMIT 200;
#     """

def get_word(word):
    return f"""
        SELECT *
        FROM words
        WHERE word = '{word}';
    """
