import pdfplumber




def pdf_to_text(path, save_path):
    text = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n\n" #indicate a page change
    with open(save_path, 'w', encoding="utf-8") as f:
        f.write(text)


def clean_text(text):
    weird_characters = ["*", "❖", "✓", "➢", "●", "♦", "❖", "✓", "〓", "•", "[", "]", "{", "}", "…", "·", "    "]
    for char in weird_characters:
        text = text.replace(char, " ")
    sentences = text.split("\n")
    out = ' '.join(sentence for sentence in sentences)
    out += "\n\n"
    return out


