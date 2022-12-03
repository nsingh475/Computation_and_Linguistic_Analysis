from __future__ import unicode_literals, print_function
import pickle
import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example

class Train_BIO_NER():
    
    """Train model to learn to generate BIO labels for each token in NLQ"""
    
    def __init__(self, train_data, labels, model, new_model_name, out_path, n_iter):
        super().__init__()
        self.train_data = train_data 
        self.labels = labels 
        self.model = model 
        self.new_model_name = new_model_name
        self.out_path = out_path 
        self.n_iter = n_iter

        
    def run(self):
        
        ## ------------------------------------- Helper functions ----------------------------------------------------------## 
        ## ------------------------------------- Main Execution ------------------------------------------------------------##
        if self.model is not None:
            mdl = spacy.load(self.model)  # load existing spacy model
            print("Loaded model '%s'" % self.model)
        else:
            mdl = spacy.blank('en')  # create blank Language class
            print("Created blank 'en' model")

        if 'ner' not in mdl.pipe_names:
            ner = mdl.create_pipe('ner')
            mdl.add_pipe('ner') # mdl.add_pipe(ner)  ### use this in case of spacy v2
        else:
            ner = mdl.get_pipe('ner')

        for i in self.labels :
            ner.add_label(i)   # Add new entity labels to entity recognizer

        if self.model is None:
            optimizer = mdl.begin_training()
        else:
            optimizer = mdl.entity.create_optimizer()

        # Get names of other pipes to disable them during training to train only NER
        other_pipes = [pipe for pipe in mdl.pipe_names if pipe != 'ner']
        with mdl.disable_pipes(*other_pipes):  # only train NER
            for itn in range(self.n_iter):
                random.shuffle(self.train_data)
                losses = {}
                batches = minibatch(self.train_data, size=compounding(4., 32., 1.001))
                for batch in batches:
                    """ Below commented code works for Spacy v2
                    texts, annotations = zip(*batch)
                    mdl.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)"""
                    for text, annotations in batch:
                        doc = mdl.make_doc(text)
                        example = Example.from_dict(doc, annotations) # create Example
                        mdl.update([example], sgd=optimizer, losses=losses, drop=0.35) # Update the model
                    
                print('Losses', losses)

        # Save model 
        if self.out_path is not None:
            output_dir = Path(self.out_path+'NER/')
            if not output_dir.exists():
                output_dir.mkdir()
            mdl.meta['name'] = self.new_model_name  # rename model
            mdl.to_disk(output_dir)
            print("Saved model to", output_dir)

            return mdl
        
class Evaluate_BIO_NER():
    
    """Train model to learn to generate BIO labels for each token in NLQ"""
    
    def __init__(self, in_path, file_name, model_path, model_name):
        super().__init__()
        self.in_path = in_path
        self.file_name = file_name
        self.model_path = model_path 
        self.model_name = model_name 
        
    def run(self):
        
        ## ------------------------------------- Helper functions ----------------------------------------------------------## 
        ## ------------------------------------- Main Execution ------------------------------------------------------------##
        
        # load BIO file
        bio_df = pd.read_csv(self.in_path+self.file_name)

        # load model
        nlp = spacy.load(self.model_path+self.model_name)

        ## 
        text_list = bio_df['NL_query'].values

        # predicting
        eval_data = []
        for txt in text_list:
            ent_list = []
            doc = nlp(txt)
            for ent in doc.ents:
                ent_list.append((ent.label_, ent.text))
            eval_data.append(ent_list)
          ## add code for accuracy
          ## add code to get the exact values

        # return accuracy, eval_data
        return eval_data