import spacy
from spacy import displacy
import json
from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
import os
import random
from spacy.training import Example
from spacy.util import minibatch
import torch



# #The old function used for training the first example
def prepare_data_set(training_file):
    """
    This prepares the data set for training, you can export to train.spacy it or use it for internal training
    :param training_file:
    :return:
    """

    with open(training_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data_set = []
    for example in data:
        text = example[0]
        entities = []
        for entity in example[1]["entities"]:
            start = entity[0]
            end = entity[1]
            label = entity[2]
            entities.append((start,end,label))
        data_set.append((text, entities))
    random.shuffle(data_set)
    return data_set

def export_for_training(train_data,export_name):
    nlp = spacy.load("en_core_web_sm")
    doc_bin = DocBin()

    for text,entities in tqdm(train_data):
        doc = nlp.make_doc(text)
        ents = []
        ent_idx = []
        for entity in entities:
            start, end, label = entity
            for start, end, label in entities:
                skip = False
                for idx in range(start, end):
                    if idx in ent_idx:
                        skip = True
                        break
                if skip:
                    continue
                ent_idx.append(start)
                ent_idx.append(end)
                try:
                    span = doc.char_span(start,end,label=label, alignment_mode="contract")
                except:
                    continue
                if span is None:
                    pass
                else:
                    ents.append(span)
        doc.ents = ents
        doc_bin.add(doc)
    doc_bin.to_disk("another_test/" + export_name + ".spacy")

def main():
    import gc
    gc.collect()
    torch.cuda.empty_cache()

    # training_file = "Data_for_Training/train_data.json"
    # export_name = "training"
    # dataset = prepare_data_set(training_file)
    # export_for_training(dataset,export_name)


    add_config = "python -m spacy init fill-config ./config/base_config.cfg ./config/config.cfg"
    os.system(add_config)
    # train_model = "python -m spacy train ./config/config.cfg\
    # --output \"C:/Users/Raymond Huang/Desktop/resume and profolio/profolio/Project Keyword AI/Models\"\
    #     --paths.train ./another_test/ --paths.dev ./another_test/ --gpu-id 0"

    train_model = "python -m spacy train ./config/config.cfg\
        --output \"C:/Users/Raymond Huang/Desktop/resume and profolio/profolio/Project Keyword AI/Models\"\
            --paths.train ./spacy_data/ --paths.dev ./spacy_data/ --gpu-id 0"
    os.system(train_model)

if __name__ == "__main__":
    main()