from pathlib import Path

abecedario ="abcdefghijklmnñopqrstuvwxyz\n"
tildes = "áéíóúü"
vocales = "aeiouu"

def standarize(word):
    new_word = ""
    for letter in word:
        if letter in abecedario:
            new_word += letter

        else:
            biyeccion = tildes.find(letter)
            if biyeccion != -1:
                new_word += vocales[biyeccion]
            else:
                print("WARNING: ",word)
    return new_word

counter=0
file_size = Path('dictionary.txt').stat().st_size
with open(r'05.txt', 'r', encoding="UTF-8") as origin:
    with open(r'dictionary.txt', 'w') as target:
        word = origin.readline()
        while word:
            target.write(standarize(word))
            counter +=1
            word = origin.readline()
