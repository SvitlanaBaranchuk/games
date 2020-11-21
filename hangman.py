# Problem Set 2, hangman.py
# Name: Svitlana Baranchuk
# Collaborators:
# Time spent: 4 evenings

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import re

# letters_guessed - list with entered letters.
letters_guessed = set([])
# guesses_remaining - attempts that are available to the user at the beginning of the game.
guesses_remaining = 6
# warnings_remaining - warnings that are available to the user at the beginning of the game.
warnings_remaining = 3

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


# end of helper code

# -----------------------------------

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
    if set(secret_word) <= set(letters_guessed):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    letter = list(secret_word)
    output_letter = []
    for l in range(len(letter)):
        if letter[l] in letters_guessed:
            output_letter.append(letter[l])
        else:
            output_letter.append('_ ')
    output = ''.join(output_letter)
    return output


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    letters = set('abcdefghijklmnopqrstuvwxyz')
    available = set(letters) - set(letters_guessed)
    available = list(available)
    available = sorted(available)
    available = ''.join(available)
    return available


def warnings_remainings(guesse, warnings_remaining):
    '''
    guesse: all leters entered by the user
    warnings_remaining: warnings that are available to the user
    '''
    if guesse in letters_guessed:
        warnings_remaining -= 1
        print("Oops! You've already guessed that letter. You now have", warnings_remaining, "warnings:",
              get_guessed_word(secret_word, letters_guessed))
        print('-' * 12)
    else:
        letters_guessed.add(guesse)
        print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        print('-' * 12)


def remaining(guesse, guesses_remaining):
    '''
    guesse: all leters entered by the user
    guesses_remaining: attempts that are available to the user
    '''
    if guesses_remaining <= 0:
        print('Sorry, you ran out of guesses. The word was else:', '"', secret_word, '"')
    else:
        letters_guessed.add(guesse)
        print('You have', guesses_remaining, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))


def guesses_remainings(guesses_remaining, warnings_remaining):
    '''
    guesses_remaining: attempts that are available to the user
    warnings_remaining: warnings that are available to the user
    '''
    while guesses_remaining >= 1:
        guesse = str(input('Please guess a letter:')).lower()
        if guesse in secret_word:
            warnings_remainings(guesse, warnings_remaining)
        else:
            if guesse in set('aeiou'):
                letters_guessed.add(guesse)
                guesses_remaining -= 2
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('-' * 12)
            elif not re.search(r'[A-Za-z]', guesse) or len(guesse) > 1:
                letters_guessed.add(guesse)
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print('Oops! That is not a valid letter. You have', warnings_remaining, 'warnings left:',
                          get_guessed_word(secret_word, letters_guessed))
                    print('-' * 12)
                elif warnings_remaining <= 0:
                    guesses_remaining -= 1
                    print('Oops! That is not a valid letter:', get_guessed_word(secret_word, letters_guessed))
                    print('-' * 12)
            else:
                letters_guessed.add(guesse)
                guesses_remaining -= 1
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('-' * 12)
        remaining(guesse, guesses_remaining)
        if set(secret_word) <= letters_guessed:
            total_score = len(secret_word) * ((6 - guesses_remaining) + (3 - warnings_remaining))
            print('-' * 12)
            print('Congratulations, you won! Your total score for this game is:', total_score)
            break


def start():
    '''
    This function contains the text that is displayed at the
    beginning of the program.
    '''
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('-' * 12)
    print('You have 6 guesses left.')
    print('Available letters:', get_available_letters(letters_guessed))


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
    start()
    guesses_remainings(guesses_remaining, warnings_remaining)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


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
    for letter in range(len(my_word)):
        if my_word[letter] != '_':
            if my_word[letter] != other_word[letter]:
                return False
            letters += other_word[letter]
        else:
            if other_word[letter] in letters:
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
    joint = ''
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word):
            joint += other_word + ' '
    print(joint)


def letters(guesses_remaining,warnings_remaining ):
    '''
    guesses_remaining: attempts that are available to the user
    warnings_remaining: warnings that are available to the user
    '''
    while guesses_remaining >= 1:
        guesse = str(input('Please guess a letter:')).lower()
        if guesse in secret_word:
            warnings_remainings(guesse, warnings_remaining)
        elif guesse == '*':
            print('Possible word matches are:')
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        else:
            if guesse in set('aeiou'):
                letters_guessed.add(guesse)
                guesses_remaining -= 2
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                print('-' * 12)
            elif not re.search(r'[A-Za-z]', guesse) or len(guesse) > 1:
                letters_guessed.add(guesse)
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print('Oops! That is not a valid letter. You have', warnings_remaining, "warnings left:",
                          get_guessed_word(secret_word, letters_guessed))
                    print('-' * 12)
                elif warnings_remaining <= 0:
                    guesses_remaining -= 1
                    print('Oops! That is not a valid letter:', get_guessed_word(secret_word, letters_guessed))
                    print('-' * 12)
            else:
                letters_guessed.add(guesse)
                guesses_remaining -= 1
                print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))
                print('-' * 12)
        remaining(guesse, guesses_remaining)
        if set(secret_word) <= letters_guessed:
            total_score = len(secret_word) * ((6 - guesses_remaining) + (3 - warnings_remaining))
            print('-' * 12)
            print('Congratulations, you won! Your total score for this game is:', total_score)
            break


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
    start()
    letters(guesses_remaining, warnings_remaining)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

 secret_word = choose_word(wordlist)
 hangman_with_hints(secret_word)
