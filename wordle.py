from random import choice, randint
from termcolor import colored as c
from os import system
clear = lambda: system('cls')

class Wordle():

    def __init__(self,
    solution_dictionary_path=r'guessesESP.txt',
    guess_dictionary_path=r'guessesESP.txt',
    frequencies_path=r'frequenciesESP.txt',
    lives=6,
    wordle_length=5,
    real_words = True
    ):
        self.wordle_length = wordle_length
        self.wordle = []
        self.lives = lives
        self.unappearing = set()
        self.word = self.chooseWord(solution_dictionary_path, guess_dictionary_path, frequencies_path)
        self.win = False
        self.real_words = real_words
        self.Guesses = []
        return

    def chooseWord(self, solution_dictionary_path, guess_dictionary_path, frequencies_path):
        if frequencies_path:
            COTA_INFERIOR, COTA_SUPERIOR = 8, 11

            with open(solution_dictionary_path,'r') as Guesses:
                with open(frequencies_path,'r') as Frequencies:
                    self.dictionary = Guesses.readlines()
                    frequencies = Frequencies.readlines()
                    zipped = [(guess, float(frequency)) for guess, frequency in zip(self.dictionary,frequencies)]
                    sorted_list = sorted(zipped, key=lambda item: item[1])
            filtered = [guess for guess,frequency in sorted_list if COTA_INFERIOR<frequency<COTA_SUPERIOR]
            word = choice(filtered)[:-1]
            self.dictionary = set(self.dictionary)
            with open(guess_dictionary_path, 'r') as f:
                self.dictionary = self.dictionary.union(set(f.readlines()))

        else:
            with open(solution_dictionary_path, 'r') as f:
                self.dictionary = f.readlines()
                word = choice(self.dictionary)[:-1]
                self.dictionary = set(self.dictionary)
            with open(guess_dictionary_path, 'r') as f:
                self.dictionary = self.dictionary.union(set(f.readlines()))

        return word

    def see(self):
        print(self.word)

    def loseLife(self):
        self.lives -= 1

    def printWordle(self):
        if self.win:
            clear()
            self.Guesses += [self.wordle]
            for guess in self.Guesses:
                for letter in guess:
                    print(letter, end = '')
                print()
            print()
            print(c("¡Felicidades!", "cyan"))
            self.lives=0
            return


        self.loseLife()

        clear()
        self.Guesses += [self.wordle]
        if self.lives:
            for guess in self.Guesses:
                for letter in guess:
                    print(letter, end = '')
                print()
            print()
            print("Intentos restantes: ", c(self.lives, 'blue'), "\n")
            print("Letras descartadas: ", self.unappearing)

    def checkWord(self, Word):
        word = Word.lower()
        abecedario = 'abcdefghijklmnñopqrstuvwxyz'
        if len(word)!=5:
            return False
        for letter in word:
            if letter not in abecedario:
                return False
        if self.real_words:
            if word+'\n' not in self.dictionary:
                return False
        return True

    def guess(self):
        guess = input().lower()
        if guess == 'exit':
            self.lives=0
            return
        correct = self.checkWord(guess)
        while not correct:
            print(c("Palabra incorrecta. Escribe de nuevo. \n"))
            guess = input().lower()
            if guess == 'exit':
                self.lives=0
                return
            correct = self.checkWord(guess)


        wordle = []

        #checks the correct letters
        for guess_letter, correct_letter in zip(guess, self.word):
            if guess_letter == correct_letter:
                wordle += [c(correct_letter.upper(), 'green')]
            else:
                wordle += ['0']

        # print("Correct letters:", wordle)

        incorrect_guess =   [] #letters not green in the guessed word
        incorrect_correct = [] #natural inyection of incorrect_guess to self.wordle
        for letter, guess_letter, correct_letter in zip(wordle, guess, self.word):
            if letter == '0':
                incorrect_guess += guess_letter
                incorrect_correct += correct_letter
        # print("Not correct letters:", incorrect_guess)
        # print("Not correct letters respective to real word:", incorrect_correct)

        incorrect_format = []


        for i in range(len(incorrect_guess)):
            if incorrect_guess[i] in incorrect_correct:                     #if the letter is in the word but not on that position
                incorrect_format += [c(incorrect_guess[i].upper(), 'yellow')]       #make it yellow
                incorrect_correct.remove(incorrect_guess[i])                #and don't take that letter in consideration from now on
            else:
                incorrect_format += incorrect_guess[i].upper()
                self.unappearing = self.unappearing.union(set(incorrect_guess[i]))


        # print("Incorrect letters formatted", incorrect_format)
        self.wordle = []
        counter = 0

        # print("wordle:",wordle)
        for i in range(len(wordle)):
            if wordle[i] == '0':
                self.wordle += incorrect_format[counter]
                counter += 1
            else:
                self.wordle += wordle[i]

        if guess == self.word:
            self.win = True
            return

    def play(self):
        while self.lives>0:
            self.guess()
            self.printWordle()
        if not self.win:
            print("La palabra era", self.word)

    def getGuessState(self):
        word = [char for char in self.wordle if char not in ['\x1b', '2', '3', 'm','[','0']]

        special_char = False
        counter = 1

        correct = [] #Green letters
        present = [] #Yellow letters
        absent = []  #Grey letters


        for i in range(len(self.wordle)):
            if special_char: #exit
                if self.wordle[i] == '\x1b':
                    special_char = False
                pass
            else:
                if self.wordle[i] == '\x1b': #enter

                    special_char = True
                    if self.wordle[i+3] == '3':
                        present.append((self.wordle[i+5], counter))
                    elif self.wordle[i+3] == '2':
                        correct.append((self.wordle[i+5], counter))
            if self.wordle[i] in word:
                counter +=1

        absent = [char for char in word if char not in [letter for letter, position in present] and char not in [letter for letter, position in correct]]
        return correct, present, absent

    def updateWordleState(self):
        correct, present, absent = self.getGuessState()

if __name__ == '__main__':
    wordle = Wordle()
    wordle.play()
input()




