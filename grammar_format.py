# TODO: Add code for assinging Part of Speech
def assign_part_of_speech(word):
    part_of_speech = word.word_class + word.sub_class + \
        word.tense + word.singular_plural + word.person
    return part_of_speech
