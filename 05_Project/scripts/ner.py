import sys
mode = sys.argv[1] ## getting argument from commandline

from library.ner_bio import *

in_path = f'Data/Input/{mode}/'
out_path = f'Data/Output/{mode}/'


if mode == 'train': ## Training NER
    labels = ['B', 'O', 'I']
    new_model_name='BIO_label'
    n_iter=10
    model = None
    BIO_obj = Train_BIO_NER(train_data, labels, model, new_model_name, out_path, n_iter)
    out_model = BIO_obj.run()
else: ## evaluating / testing NER
    model_path =  f'Data/model/'
    file_name = 'BIO_labels_SpaCy.csv'
    model_name = 'NER_BIO'
    NER_Obj = Evaluate_BIO_NER(out_path, file_name, model_path, model_name)
    eval_data = NER_Obj.run() # accuracy, eval_data = NER_Obj.run()
    