# Problem Set 2, hangman.py
# Name: Svitlana Baranchuk
# Collaborators:
# Time spent: 9 evenings and 3 mornings

# Hangman Game
import random
import string
from enum import Enum

# Constants for the game.
WORDLIST_FILENAME = "words.txt"
# GUESSES_INITIAL - start value for guesses_remaining.
GUESSES_INITIAL = 6
# WARNINGS_INITIAL - start value for warnings_remaining.
WARNINGS_INITIAL = 3
VOWELS = set('aeiou')
# BORDER_LENGTH - the number of dashes to separate information.
BORDER_LENGTH = 12
UNEXPECTED_LETTER = '_ '


class GameMode(Enum):
    '''
    The class contains game options:
    1 - without hints and 2 - with hints
    '''
    WITHOUT_HINTS = 1
    WITH_HINTS = 2


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()
secret_word = choose_word(wordlist)


def is_word_guessed(letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: set (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: set (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    output_letter = ' '
    letter = list(secret_word)
    output_letter = output_letter.strip()
    output_letter = list(output_letter)
    for i in range(len(letter)):
        if letter[i] in letters_guessed:
            output_letter.append(letter[i])
        else:
            output_letter.append(UNEXPECTED_LETTER)
    return ''.join(output_letter)


def get_available_letters(letters_guessed):
    """
    letters_guessed: set (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    available = []
    for i in string.ascii_lowercase:
        if not i in letters_guessed:
            available.append(i)
    return ''.join(available)


def text_warnings_remainings(guesse, warnings_remaining, letters_guessed):
    '''
    warnings_remaining: warnings that are available to the user
    letters_guessed: a set of letters that the user enters

    The text_warnings_remainings(warnings_remaining) function
    determines whether a user has entered a specific entered letter.
    If so, one warning about the already entered letter is removed;
    if not, the program goes on.
    '''
    letters_guessed.add(guesse)
    if warnings_remaining > 0:
        print(f"Oops! You've already guessed that letter. You now have {warnings_remaining} warnings:",
              get_guessed_word(letters_guessed))
        print('-' * BORDER_LENGTH)
    else:
        print("Oops! You've already guessed that letter.You have no warnings left so you lose one guess:", get_guessed_word(letters_guessed))
        print('-' * BORDER_LENGTH)


def text_good_guess(guesse, letters_guessed):
    '''
    guesse: all leters entered by the user
    letters_guessed: a set of letters that the user enters

    This function contains the text that will be displayed
    if the user guesses the letter.
    '''
    letters_guessed.add(guesse)
    print('Good guess:', get_guessed_word( letters_guessed))
    print('-' * BORDER_LENGTH)


def text_no_valid_letter(warnings_remaining, letters_guessed):
    '''
    warnings_remaining: warnings that are available to the user
    letters_guessed: a set of letters that the user enters

    This function contains text that will be displayed if the
    user runs out of all warnings about incorrect letter entry.
    '''
    if warnings_remaining >= 0:
        print(f'Oops! That is not a valid letter. You have {warnings_remaining} warnings left:',
              get_guessed_word(letters_guessed))
        print('-' * BORDER_LENGTH)
    else:
        print('Oops! That is not a valid letter. You have no warnings left so you lose one guess:',
              get_guessed_word(letters_guessed))
        print('-' * BORDER_LENGTH)



def text_not_in_word(guesse, letters_guessed):
    '''
    letters_guessed: a set of letters that the user enters

    This function contains text that will be displayed if the user
    does not guess the letter, ie enters a letter that is not in the word.
    '''
    letters_guessed.add(guesse)
    print("Oops! That letter is not in my word:", get_guessed_word( letters_guessed))
    print('-' * BORDER_LENGTH)


def information(guesses_remaining, letters_guessed):
    '''
    guesses_remaining: attempts that are available to the user
    letters_guessed: a set of letters that the user enters

    The function information(guesses_remaining) contains the text that
    which contains information about the user's attempts and the
    remaining letters.
    '''
    print(f'You have {guesses_remaining} guesses left.')
    print('Available letters:', get_available_letters(letters_guessed))


def welcome_message():
    '''
    This function contains the text that is displayed
    at the beginning of the game.
    '''
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('-' * BORDER_LENGTH)


def game_iterations(guesses_remaining, game_mode, warnings_remaining, letters_guessed):
    '''
    guesses_remaining: attempts that are available to the user
    game_mode: from class GameMode
    warnings_remaining: warnings that are available to the user
    letters_guessed - set with entered letters

    The game_iterations(guesses_remaining, warnings_remaining, game_mode) function
    determines whether the entered letter is in the word. If so - the
    program moves on. If not, this letter is a vowel - two attempts
    are deleted, if a consonant - one attempt. If a character is entered,
    a warning and their number are displayed. At the end of the number
    of warnings, one attempt is deleted.
    If the word is guessed, a greeting message is displayed.
    '''
    while guesses_remaining > 0 and not is_word_guessed(letters_guessed):
        information(guesses_remaining, letters_guessed)
        guesse = (input('Please guess a letter:')).lower()
        guesse = guesse.zfill(1)

        # Conditions to be met on the entered "*"
        if guesse == '*' and game_mode == GameMode.WITH_HINTS:
            show_possible_matches(get_guessed_word(letters_guessed))
            continue

        # Conditions for the presence of the twice entered letter.
        if guesse in letters_guessed:
            warnings_remaining -= 1
            if warnings_remaining <= 0:
                guesses_remaining -= 1
            text_warnings_remainings(guesse, warnings_remaining, letters_guessed)

        # Conditions for the presence of the entered letter in the word.
        elif guesse in secret_word:
            text_good_guess(guesse, letters_guessed)

        # Conditions to be met on the entered symbol or letter not in the word.
        elif not guesse.isascii() or not guesse.isalpha() or len(guesse) != 1:
            warnings_remaining -= 1
            if warnings_remaining < 0:
                guesses_remaining -= 1
            text_no_valid_letter(warnings_remaining, letters_guessed)
        else:
            if guesse in VOWELS:
                guesses_remaining -= 2
                text_not_in_word(guesse, letters_guessed)
            else:
                guesses_remaining -= 1
                text_not_in_word(guesse, letters_guessed)

    return warnings_remaining, guesses_remaining


def calculating_score(guesses_remaining):
    '''
    This function calculates the value total_score
    in conditions of victory.
    '''
    return guesses_remaining * len(set(secret_word))


def game_results(guesses_remaining, letters_guessed, secret_word):
    '''
    This function contains text to end the game.
    '''
    if is_word_guessed(letters_guessed):
        print(f'Congratulations, you won! Your total score for this game is: {calculating_score(guesses_remaining)}')
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')


def hangman(guesses_remaining, warnings_remaining, game_mode=GameMode.WITHOUT_HINTS):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = set()

    # The course of the game.
    welcome_message()
    warnings_remaining, guesses_remaining = game_iterations(guesses_remaining, game_mode, warnings_remaining, letters_guessed)
    game_results(guesses_remaining, letters_guessed, secret_word)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    if len(my_word) != len(other_word):
        return False

    letters_guessed = set(my_word) - {UNEXPECTED_LETTER.strip()}
    for i in range(0, len(my_word)):
        if my_word[i] == UNEXPECTED_LETTER.strip() and other_word[i] in letters_guessed:
            return False
        if my_word[i] != UNEXPECTED_LETTER.strip() and my_word[i] != other_word[i]:
            return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    possible_matches = []
    my_word = my_word.replace(' ', '')
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    if len(possible_matches) != 0:
        print('Possible word matches are:')
        print(' '.join(possible_matches))
    else:
        print('No matches found')
    print('-' * BORDER_LENGTH)


def hangman_with_hints():
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    hangman(GUESSES_INITIAL, WARNINGS_INITIAL, game_mode=GameMode.WITH_HINTS)


if __name__ == "__main__":
    hangman_with_hints()