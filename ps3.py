# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Svitlana Baranchuk
# Collaborators : -
# Time spent    : 2 evenings and 5 hour

import math
import random
import string

# Constants for the game.
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'
# BORDER_LENGTH - the number of dashes to separate information.
BORDER_LENGTH = 8
END = '!!'
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
WORDLIST_FILENAME = 'words.txt'


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print('Loading word list from file...')
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print('  ', len(wordlist), 'words loaded.')
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score = 0
    second_component = (HAND_SIZE * len(word.lower()) - 3 * (n - len(word.lower())))

    for letter in word:
        score += SCRABBLE_LETTER_VALUES.get(letter.lower(), 0)

    if score > second_component:
        second_component = 1

    return score * second_component


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    print('Current Hand:', end=' ')
    for letter in hand.keys():
        for i in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    hand[WILDCARD] = 1

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    new_hand = {}
    word = word.lower()
    new_word = get_frequency_dict(word)

    for letter in hand.keys():
        if hand[letter] - new_word.get(letter, 0) > 0:
            new_hand[letter] = hand[letter] - new_word.get(letter, 0)

    return new_hand


def is_word_from_hand(hand, word):
    '''
    This function check if there is a letter in word in hand.
    Returns True if letter in word in hand. Otherwise, returns False.
    '''
    for letter in word.lower():
        if letter not in hand:
            return False
        else:
            return True


def is_word_exists(word, hand, word_list):
    """
    Returns True if word is in the word_list. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    new_hand = hand.copy()

    # Check word in word_list.
    if word.lower() in word_list:
        for letter in word.lower():
            if letter in new_hand:
                new_hand[letter] -= 1
                if new_hand[letter] == -1:
                    return False
            else:
                return False
        return True

    # Check wildcard in word.
    elif WILDCARD in word and WILDCARD in new_hand:
        wildcards = []
        for letter in range(len(word)):
            if word[letter] == WILDCARD:
                wildcards.append(letter)

        if len(wildcards) > 1:
            return False

        for vowel in VOWELS:
            if word.replace(WILDCARD, vowel) in word_list:
                return True

    else:
        return False


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """
    # total_score - score for all guesse word in hand.
    # word_score - score for one guesse word.
    total_score = 0
    word_score = 0

    while calculate_handlen(hand) > 0:
        # Start game.
        display_hand(hand)

        guesses_word = (input(f'Enter word, or “{END}” to indicate that you are finished: ')).lower()
        # First conditions for end the game.
        if guesses_word == END:
            break

        if is_word_exists(guesses_word, hand, word_list) and is_word_from_hand(hand, guesses_word):
            word_score += get_word_score(guesses_word, calculate_handlen(hand))
            total_score += word_score
            print(f'"{guesses_word}" earned {word_score} points. Total: {total_score} points\n')
        else:
            print('This is not a valid word. Please choose another word.\n')

        hand = update_hand(hand, guesses_word)

        # Second conditions for end the game.
    if calculate_handlen(hand) <= 0:
        print('Ran out of letters')

    print(f'Total score for this hand: {total_score}')
    print('-' * BORDER_LENGTH)
    return total_score


def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()

    available = []
    for let in string.ascii_lowercase:
        if let not in new_hand:
            available.append(let)

    new_letter = random.choice(available)
    new_hand[new_letter] = new_hand.pop(letter)

    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    # final_score - score for all guesse word in all hand.
    final_score = 0
    number_hands = int(input('Enter total number of hands: '))

    for _ in range(number_hands):
        hand = deal_hand(HAND_SIZE)

        display_hand(hand)

        substitute_letter = (input('\nWould you like to substitute a letter? ')).lower()
        if substitute_letter == 'yes':
            letter = input('Which letter would you like to replace: ')
            print()  # print an empty line
            hand = substitute_hand(hand, letter)
        else:
            print()  # print an empty line

        hand_score = play_hand(hand, word_list)

        replay_hand = (input('Would you like to replay the hand? ')).lower()
        if replay_hand == 'yes':
            print()  # print an empty line
            new_hand_score = play_hand(hand, word_list)
            if hand_score < new_hand_score:
                hand_score += new_hand_score

        final_score += hand_score
    print('Total score over all hands: ', final_score)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
