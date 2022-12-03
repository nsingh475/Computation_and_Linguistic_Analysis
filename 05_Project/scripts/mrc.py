import sys
from google.colab import files
mode = sys.argv[1] ## getting argument from commandline

from library.mrc_bert import *


in_path = f'Data/Input/{mode}/'
out_path = f'Data/Output/{mode}/'
model_path = f'Data/model/BERT/'
enc_path = out_path + 'batch_encoding/'
iterations_before_saving_model = 20 ## intermediate model will be save after processing 50 batches from the loader

if mode == 'train':
    num_chunks = 4   ## number of chunks in which encoding data is chunked 
    num_epochs = 2 ## number of epochs
else:
    num_chunks = 1
    num_epochs = 1

save_model_name = 'bert-qa'

## loading BERT encodings
batch_size = 128
model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad' ## pre-trained model
freeze_layer_count = 439 
lr=5e-5 ## learning rate
mdl = None

for epoch in range(num_epochs):
    print(f'------ Epoch {epoch+1} ------')
    for chunk in range(num_chunks):
        print(f'---- Working with chunk {chunk+1} ----')
        encoding_file = f'batch_encoding_{chunk+1}.pickle'
        batch_encoding = pd.read_pickle(enc_path+encoding_file)
        batch_loader = []
        for encodings in batch_encoding:
            train_df = Transform_wikiSQLDataset(encodings)
            loader = torch.utils.data.DataLoader(train_df, batch_size, shuffle=True)
            batch_loader.append(loader)

        if mode == 'train':  ## training BERT based MRC
            BERT_MRC_obj = Train_BERT_MRC(model_path, batch_loader, freeze_layer_count, model_name, save_model_name, lr, iterations_before_saving_model, mdl)
            mdl, out_model = BERT_MRC_obj.run()
            ## dowload mdl in local
            files.download(model_path+save_model_name)
        else:  ## evaluating / testing MRC
            BERT_MRC_obj = Evaluate_BERT_MRC(model_path, save_model_name, batch_loader)
            accuracy ,eval_data = BERT_MRC_obj.run()