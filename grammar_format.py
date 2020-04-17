# def get_state():
#     present_state = {
#         'first': {
#             'class': 5,
#             'sub_class': 9,
#             'singular_plural': 1,
#             'person': 1
#         },
#         'second': {
#             'class': 2,
#             'sub_class': 12,
#             'tense': 'present',
#             'word': 'am'
#         },
# 'third': {
# 	'word': {}
# }
# }


def assign_part_of_speech(word):
    part_of_speech = word.word_class + word.sub_class + \
        word.tense + word.singular_plural + word.person
    return part_of_speech
