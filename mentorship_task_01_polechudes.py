import random


# function to replace '_' with the letter if it exists in word we are trying to guess

def guess_letter(entered_letter, before_guess, word):
    i = 0
    for letter in word:
        if letter == entered_letter:
            before_guess = before_guess[:i] + entered_letter + before_guess[i+1:]
        i += 2
    if entered_letter not in word:
        print('No luck, the letter "' + entered_letter + '" is not in this word. Try again.')
    return before_guess

# defining function that has all the actions in game

def play_game():

    print('Hello user! Let\'s play a game of Pole Chudes')

    # ask user to select the number and save it, number will correspond to line in words dictionary
    # when empty response received random number will be selected

    while True:
        selected_number = input('Please enter any integer number to select a word or just press \'Enter\' and word will be selected randomly: ')
        try:
            if len(selected_number) == 0:
                selected_number = random.randint(0, len(words))
            else:
                selected_number = int(selected_number)
            break
        except:
            print('Looks like you entered something different than integer number')

    # pick the word with corresponding number from dictionary and mask it with '_ '
    # whitespace is added to underscore so it's easier for user to count hidden letters

    i = 0
    for word in words:
        if i == selected_number % len(words):
            word_to_guess = word.rstrip('\n').upper()
        i += 1

    masked_word = '_ ' * len(word_to_guess)

    print('Great! Now we have the word to guess: ', masked_word)

    # here we start actually playing, we read letter entered by user and reveal it if guess is correct
    # game continues while there there is at least 1 letter that was not guessed

    attempts_no = 0
    while '_' in masked_word:
        user_letter=input('Please enter the letter: ')
        if user_letter.upper() == 'QUIT':
            break
        elif len(user_letter) > 1:
            print('You entered more than 1 character. Don\'t try to cheat. Only one letter is allowed per attempt :)')
        elif user_letter.isdigit() is True:
            print('Words do not contain numbers. It will not be counted as an attempt :)')
        else:
            masked_word = guess_letter(user_letter.upper(), masked_word, word_to_guess)
            print(masked_word)
            attempts_no += 1

    if user_letter.upper() == 'QUIT':
        print('So sorry to see you quit :(. You gave up after', str(attempts_no), 'attempts.\nIf you would like to try the same word later it\'s number is', str(selected_number) + '.')
    else:
        print('\nGreat job! You guessed the word', word_to_guess, 'in', str(attempts_no), 'attempts. Congratulations!')
        print('This word has number', str(selected_number) + '.', 'Note this number so you can ask your friends to guess the same word later.\n\nLet\'s see how many attempts they use ;)')


# opening the file and reading all the words
# it is assumed that each line in file is a word

try:
    inp_dict = open('dict.txt', 'r')
    words = inp_dict.readlines()
    play_game()
except:
    print('Looks like file with words for the game is missing from the folder.\nPlease make sure to have dict.txt file within the same folder as a game itself.')


