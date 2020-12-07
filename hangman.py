# Problem Set 2, hangman.py
# Name: Svitlana Baranchuk
# Collaborators:
# Time spent: 9 evenings

# Hangman Game
import random
import string
from enum import Enum

WORDLIST_FILENAME = "words.txt"


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


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    letter = list(secret_word)
    output_letter = []
    for i in range(len(letter)):
        if letter[i] in letters_guessed:
            output_letter.append(letter[i])
        else:
            output_letter.append('_ ')
            if output_letter[-1] == ' ':
                output_letter = output_letter[:-1]
    return ''.join(output_letter)


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    available = ""
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available = available + letter
    return available


def text_warnings_remainings(warnings_remaining, letters_guessed):
    '''
    warnings_remaining: warnings that are available to the user
    letters_guessed = set([]): a set of letters that the user enters

    The text_warnings_remainings(warnings_remaining) function
    determines whether a user has entered a specific entered letter.
    If so, one warning about the already entered letter is removed;
    if not, the program goes on.
    '''
    if warnings_remaining > 0:
        print(f"Oops! You've already guessed that letter. You now have {warnings_remaining} warnings:",
              get_guessed_word(secret_word, letters_guessed))
        print('-' * n)
    else:
        print("Oops! You've already guessed that letter.", get_guessed_word(secret_word, letters_guessed))
        print('-' * n)


def text_good_guess(guesse, letters_guessed):
    '''
    guesse: all leters entered by the user
    letters_guessed = set([]): a set of letters that the user enters

    This function contains the text that will be displayed
    if the user guesses the letter.
    '''
    letters_guessed.add(guesse)
    print('Good guess:', get_guessed_word(secret_word, letters_guessed))
    print('-' * n)


def text_no_valid_letter(warnings_remaining, letters_guessed):
    '''
    warnings_remaining: warnings that are available to the user
    letters_guessed = set([]): a set of letters that the user enters

    This function contains text that will be displayed if the
    user runs out of all warnings about incorrect letter entry.
    '''
    if warnings_remaining > 0:
        print(f'Oops! That is not a valid letter. You have {warnings_remaining} warnings left:',
              get_guessed_word(secret_word, letters_guessed))
        print('-' * n)
    else:
        print('Oops! That is not a valid letter:', get_guessed_word(secret_word, letters_guessed))
        print('-' * n)


def finish_text(guesses_remaining, letters_guessed):
    '''
    guesses_remaining: attempts that are available to the user
    letters_guessed = set([]): a set of letters that the user enters

    The function finish_text(guesse, guesses_remaining, warnings_remaining)
    displays the final text of the program. If the user wins, the function
    will display a greeting; if lost - the corresponding message.
    '''
    if is_word_guessed(secret_word, letters_guessed):
        total_score = len(secret_word) * guesses_remaining
        print(f'Congratulations, you won! Your total score for this game is: {total_score}')
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')


def text_not_in_word(letters_guessed):
    '''
    letters_guessed = set([]): a set of letters that the user enters

    This function contains text that will be displayed if the user
    does not guess the letter, ie enters a letter that is not in the word.
    '''
    print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
    print('-' * n)


class GameMode(Enum):
    '''
    The class contains game options:
    1 - without hints and 2 - with hints
    '''
    without_hints = 1
    with_hints = 2


def information(guesses_remaining, letters_guessed):
    '''
    guesses_remaining: attempts that are available to the user
    letters_guessed = set([]): a set of letters that the user enters

    The function information(guesses_remaining) contains the text that
    which contains information about the user's attempts and the
    remaining letters.
    '''
    print(f'You have {guesses_remaining} guesses left.')
    print('Available letters:', get_available_letters(letters_guessed))


def game_iterations(guesses_remaining, warnings_remaining, game_mode, letters_guessed):
    '''
    guesses_remaining: attempts that are available to the user
    warnings_remaining: warnings that are available to the user
    letters_guessed - list with entered letters
    game_mode: from class GameMode
    letters_guessed = set([]): a set of letters that the user enters

    The game_iterations(guesses_remaining, warnings_remaining, game_mode) function
    determines whether the entered letter is in the word. If so - the
    program moves on. If not, this letter is a vowel - two attempts
    are deleted, if a consonant - one attempt. If a character is entered,
    a warning and their number are displayed. At the end of the number
    of warnings, one attempt is deleted.
    If the word is guessed, a greeting message is displayed.
    '''
    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        information(guesses_remaining, letters_guessed)
        guesse = (input('Please guess a letter:')).lower()
        if guesse in secret_word:
            # Conditions for the presence of the entered letter in the word.
            if guesse in letters_guessed:
                warnings_remaining -= 1
                if warnings_remaining <= 0:
                    guesses_remaining -= 1
                text_warnings_remainings(warnings_remaining, letters_guessed)
            else:
                text_good_guess(guesse, letters_guessed)

        # Conditions to be met on the entered "*".
        elif guesse == '*' and game_mode == GameMode.with_hints:
            show_possible_matches(get_guessed_word(secret_word, letters_guessed), guesses_remaining)
            continue

        # Conditions of entered symbol.
        elif not guesse.isascii() or not guesse.isalpha() or len(guesse) != 1:
            if warnings_remaining > 0:
                warnings_remaining -= 1
            elif warnings_remaining <= 0:
                guesses_remaining -= 1
            text_no_valid_letter(warnings_remaining, letters_guessed)
        else:
            if guesse in 'aeiou':
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            text_not_in_word(letters_guessed)


def start_text():
    '''
    This function contains the text that is displayed at the
    beginning of the program.
    '''
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('-' * n)


def hangman(secret_word):
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
    # Constants for the game.
    guesses_remaining = 6
    warnings_remaining = 3
    game_mode = GameMode.without_hints
    letters_guessed = set([])

    # Functions for the game working.
    start_text()
    game_iterations(guesses_remaining, warnings_remaining, game_mode, letters_guessed)
    finish_text(guesses_remaining, letters_guessed)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word = my_word.replace(' ', '')
    letters = ''
    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] != '_':
            if my_word[i] != other_word[i]:
                return False
            letters = letters + other_word[i]
        else:
            if other_word[i] in letters:
                return False
    return True


def show_possible_matches(my_word, guesses_remaining):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    print('Possible word matches are:')
    print(" ".join(possible_matches))
    print('-' * n)


def hangman_with_hints(secret_word):
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
    # Constants for the game.
    guesses_remaining = 6
    warnings_remaining = 3
    game_mode = GameMode.with_hints
    letters_guessed = set([])

    # Functions for the game working.
    start_text()
    game_iterations(guesses_remaining, warnings_remaining, game_mode, letters_guessed)
    finish_text(guesses_remaining, letters_guessed)


if __name__ == "__main__":
    # n - the number of dashes to separate information
    n = 12

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)