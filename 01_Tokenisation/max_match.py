import sys

## Creating Japanese word list
word_list = []
for line in open(sys.argv[1]).readlines():
    row = line.split('\t')
    if len(row) == 10:
        word_list.append(row[2])
word_list_unique = list(set(word_list))
print(len(word_list_unique))

## max_match
for line in open(sys.argv[2]).readlines():
    line = line[9:-1]
    print('Line = ', line)
    tokens = []
    ## some condition to extract only full text lines
    i=0
    while i<len(line):
        max_word = ""
        for j in range (i, len(line)):
            temp_word = line[i:j+1]
            if temp_word in word_list_unique and len(temp_word)>len(max_word):
                max_word = temp_word
        if max_word == "":
            max_word = line[i]
        i = i+len(max_word)
        if max_word != '\n':
            tokens.append(max_word)
    print('Token = ', tokens)
    print('\n')

exit()
