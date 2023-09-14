


with open(r'eng\possible solutions.txt','r') as f:
    text = f.readline()

text = text.replace('\"','').replace(' ','').replace(r'\xf1','ñ').split(',')

text = [word+'\n' for word in text if '-' not in word]


with open(r'solutionsENG.txt', 'w') as f:
    f.writelines(text)
#
# with open(r'Wordle\guessesLEWDLE.txt', 'r') as f:
#     print(len(f.readlines()))
