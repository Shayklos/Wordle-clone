from wordle import *
from wordleDataScience import countLetters, findBestWord

dictionary = [word[:-1].upper() for word in Wordle().dictionary]
with open(r'dictionary.txt','r') as f:
    words = f.readlines()
    dictionary = [word[:-1].upper() for word in words]



def filterCorrect(correct, dictionary = dictionary):
    filteredList = []
    for word in dictionary:
        counter = 0
        for letter, position in correct:
            if word[position-1] != letter:  #unsatisfying word
                continue
            else:
                counter +=1                 #+1 if such letter is in the correct place
        if counter == len(correct):         #if it verifies for all letters in list correct
            filteredList.append(word)

    return(filteredList)
#[('E',1), ('A',3)]
def filterPresent(present, dictionary = dictionary):
    filteredList = []
    for word in dictionary:
        counter = 0
        for letter, position in present:
            if letter not in word:          #if the letter is not in the word, continue
                continue
            if word[position-1] == letter:  #if the letter is in the word, but in the incorrect place
                continue
            else:
                counter +=1                 #verifies for a letter
        if counter == len(present):         #if it verifies for all letters in list present
            filteredList.append(word)

    return(filteredList)

def filterAbsent(absent, dictionary = dictionary):
    filteredList = []
    for word in dictionary:             #for each word, check if it doesnt have
        for letter in absent:           #... any of the letters in absent list
            if letter in word:
                break
        else:                           #if it leaves normally the for-loop, word meets criteria
            filteredList.append(word)

    return filteredList

def filterFromClues(correct, present, absent, dictionary = dictionary):
    correctConsidered = filterCorrect(correct, dictionary) #fixes green letters
    presentConsidered = filterPresent(present, correctConsidered) #eliminate words

    correctLetters = [letter for letter, _ in correct]
    presentLetters = [letter for letter, _ in present]

    doubleLetters = []
    #e.g.: if there are two yellow 'A' means there are two 'A';
    #consider all the words with two or more 'A' only.
    for letter in presentLetters:
        if presentLetters.count(letter) > 1:
            count = presentLetters.count(letter)
            for word in presentConsidered:
                if word.count(letter) >= count:
                    doubleLetters.append(word)

    if doubleLetters:
        presentConsidered = doubleLetters

    #e.g.: if there are a yellow and a grey 'A' means there is only one 'A';
    #consider all the words with exactly one 'A' only.
    absentAndPresent = []
    absentAndPresentLetters = []
    for letter in presentLetters:
        if letter in absent:
            absentAndPresentLetters.append(letter)
            count = presentLetters.count(letter)
            for word in presentConsidered:
                if word.count(letter) == count:
                    absentAndPresent.append(word)

    if absentAndPresent:
        presentConsidered = absentAndPresent

    safeLettersToDiscard = [letter for letter in absent if letter not in list(set(absentAndPresentLetters+correctLetters))]
    finalList = filterAbsent(safeLettersToDiscard, presentConsidered)
    return finalList


## Hay que distinguir intentos pasados del actual, ya que los procesos lógicos que se
## a los que se puede llegar sabiendo que  present = [('E',2), ('E',3)] son distintos a los
## que se puede llegar si present.old = [('E',2)] y present.new = [('E',3)] (¿Quizá solo
## guardar dictionary de pasados intentos?)

## También estaría bien considerar que si se sabe que ('A', 5) está en correct, no es
## necesario elegir una palabra que acabe en A, y usar ese lugar para hallar información
## sobre otras letras que pueden estar en la palabra.

## Búsqueda de patrones. Inferir de la lista obtenida información nueva. Por ejemplo, con
## absent = list("ROATEY")
## correct = [('S',1), ('I',3)]
## present= [('L',2)]
## En el diccionario inglés, todas las palabras acaban en 'LL',
## o si list absent = list("RAE"), la penúltima letra siempre es 'L'

## De manera más avanzada, a partir de la lista obtenida, hallar una palabra que aunque
## no se adhiera a las listas absent, correct, present, si sea capaz de eliminar una gran
## cantidad de posibilidades y/o reunir una gran cantidad de información.

absent = list("ILV")
correct = []
present= [("A",2),("A",1),("N",3),("N",5),("C",4)]

for word in sorted(list(set(filterFromClues(correct,present,absent)))):
    print(word.lower() + ', ', end=' ')
