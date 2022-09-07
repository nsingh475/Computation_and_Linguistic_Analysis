Practical 00

1. Count word initial consonant sequences

    sed 's/[^a-zA-Z]\+/\n/g' < wiki.txt | sed ‘s[AEIOUaeiou][A-Za-z]*//g’ < wiki.txt | sort -r | uniq -c > initial-consonants.hist

  - Tokenize word
    sed 's/[^a-zA-Z]\+/\n/g' < wiki.txt
    This command will take the text from wiki.txt file and tokenize it
  - deleted the vowel and rest of the word
    sed ‘s/[AEIOUaeiou][A-Za-z]*//g’
    This command will replace the first vowel and the following consonants in a word by empty string
  - Sort
    Sort -r 
    This command will sort the words in reverse order (z to a)
  - Count
  uniq -c > initial-consonants.hist


2. Count word final consonant sequences

    sed ‘s/[^a-zA-Z]\+/\n/g’ < wiki.txt| rev | sed ‘s[AEIOUaeiou][A-Za-z]*//g’ | rev | sort -r | uniq -c > final-consonants.hist

  rev will reverse the word




Note:
  - Wiki Corpus Extracted from jvwiki-20220901-pages-articles.xml.bz2
  - To take an input file (wiki.txt for out case): < 
  - To store output in a file (initial-consonants.hist and final-consonants.hist): >
  - To connect the output of one program to the input of the next: | 
