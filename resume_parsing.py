from PDF2Text import pdf_to_text,clean_text
import spacy

if __name__ == "__main__":
    path = r"C:\Users\Raymond Huang\Desktop\resume and profolio\resume\Raymond Huang Old Resume Updated.pdf"
    save_path = r"./Raymond_resume.txt"
    read_path = save_path
    pdf_to_text(path,save_path)
    with open(read_path,'r',encoding='utf-8') as f:
        text = f.read()
    text = clean_text(text)

    model = r"C:\Users\Raymond Huang\Desktop\resume and profolio\profolio\Project Keyword AI\Keywords\saved_trained_models\Transformer_ner"
    nlp = spacy.load(model)
    doc = nlp(text)
    for ent in doc.ents:
        print(ent,ent.label_)