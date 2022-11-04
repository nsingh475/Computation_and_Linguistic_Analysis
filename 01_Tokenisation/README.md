# Sentence Segmentation

I have implemented the task of Sentence Segmentation using two approaches:
- Rule Based: Pragmatic segmenter
- Machine Learning Based: NLTK Punct

Files:
- Input File: Input_wiki_10_para_20plus_words.txt (I have only used first 10 paragraphs which has the more than 20 words in it)
- Output Files: pragmetic_segmenter_output.txt and nltk_segmenter_output.txt

More details on the segmenter and their performance can be found in the SentenceSegmentation.pdf file.


# Tokenization

I implemented the task of tokenization on UD treebank for Japanese using the max-match algorithm.

Files:
- Raw File: ja_gsd-ud-train.conllu from http://github.com/UniversalDependencies/
- Input File: japaneses_corpus_to_be_tokenized.txt  (after some preprocessing)
- Output File: tokenized_japanese_corpus.txt
