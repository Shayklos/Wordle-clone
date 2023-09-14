from itertools import combinations

dictionary = r'guessesESP.txt'

with open(dictionary) as wordle:
    words = wordle.readlines()
    words = [word[:-1] for word in words]


def main():
    print(countLetters())

def countLetters(dictionary=dictionary, unique = False):
    """
    Goes through the words of dictionary and returns a list of the characters of the
    words together with the number of times the characters appear, sorted by frequency.

    If unique = True, then if there are repeated letters in a word, it will only count that letter once
    """
    with open(dictionary) as wordle:
        words = wordle.readlines()
        words = [word[:-1].upper() for word in words] #to remove \n

        letras = []
        frecuencias = []
        for word in words:
            if unique:
                for letra in list(set(word)):
                    if letra in letras:
                        frecuencias[letras.index(letra)] += 1
                    else:
                        letras.append(letra.upper())
                        frecuencias.append(1)
            else:
                for letra in word:
                    if letra in letras:
                        frecuencias[letras.index(letra)] += 1
                    else:
                        letras.append(letra.upper())
                        frecuencias.append(1)



        sorted_list = sorted(zip(letras, frecuencias), key=lambda item: -item[1])
    return sorted_list

def printZipped(zipped):
    for letra, frecuencia in zipped:
        print(letra, frecuencia)

def findBestWordOld(zipped):
    """
    Brute force approach.
    For all words with different letters, calculates de sum of the frequency of their letters.

    Returns the list ranked

    """
    letras = [letra for letra, frecuencia in zipped]
    frecuencias = [frecuencia for letra, frecuencia in zipped]

    words = []

    vocales = 'aeiou'
    counter = 0
    for combination in combinations(letras, 5):
        counter += 1
        hasVowel = False
        for vowel in vocales:
            if vowel in combination:
                hasVowel = True
                word = existWordWith(combination)
                break
        if hasVowel and word:
            weight = 0
            for letter in word:
                weight += frecuencias[letras.index(letter)]
            words.append((word, weight))

        if counter%1234 == 43:
            print(f"{counter}/80730")


    return sorted(words, key=lambda item: -item[1])

def findBestWord(zipped, dictionary=dictionary, words = None):
    """
    Faster than findBestWordOld and includes repeats
    """
    if not words:
        with open(dictionary) as wordle:
            words = wordle.readlines()
            words = [word[:-1].upper() for word in words]

    letras = [letra for letra, frecuencia in zipped]
    frecuencias = [frecuencia for letra, frecuencia in zipped]

    result = []

    def sumFreq(unlisted_word, letras=letras, frecuencias=frecuencias):
        word = list(unlisted_word)
        suma = 0
        for letter in word:
            suma += frecuencias[letras.index(letter)]
        return suma

    for word in words:
        if len(set(word)) == 5:

            result.append((word, sumFreq(word)))

    return sorted(result, key=lambda item: -item[1])

def existWordWith(letters, dictionary=dictionary, words = words, exhaustive=False):
    """
    Given an array of char (eg.: list('idiot')) returns a word that has all the
    letters in that array. If it doesn'f find one, returns False. If exhaustive=True,
    returns all an array of words that verify that condition.
    """

    if not words:
        with open(dictionary) as wordle:
            words = wordle.readlines()
            words = [word[:-1] for word in words]

    if exhaustive:
        Words = []
    for word in words:
        exists = 0
        for letter in letters:
            if letter not in word:
                continue
            else:
                exists += 1
        if exists == 5:
            if exhaustive:
                Words.append(word)
            else:
                return word
    if exhaustive and Words:
        return Words
    else:
        return False
    return False

def positionRanking(char, dictionary=dictionary, words = words, return_frequencies = False):
    if not words:
        with open(dictionary) as wordle:
            words = wordle.readlines()
            words = [word[:-1] for word in words]


    frequencies = [0 for char in words[0]]

    for word in words:
        for i in range(len(word)):
            if word[i] == char:
                frequencies[i] += 1


    if return_frequencies:
        return frequencies
    else:
        s = list(sorted(frequencies))
        ranking = [s.index(i)+1 for i in frequencies]

        return ranking

def bestAnagram(letters, dictionary=dictionary):
    words = [word for word in existWordWith(list(letters), exhaustive=True)]
    results = []
    for word in words:
        score = 0
        for i in range(len(word)):
            score += positionRanking(word[i])[i]
        results.append((word,score))

    return sorted(results, key=lambda item: -item[1])






























if __name__ == '__main__':
    main()
