import torch
from transformers import RagTokenizer, RagModel
from spellchecker import SpellChecker
from textblob import TextBlob

# Load pre-trained RAG model and tokenizer
tokenizer = RagTokenizer.from_pretrained('facebook/rag-token-base')
model = RagModel.from_pretrained('facebook/rag-token-base')

# Load SpellChecker
spell = SpellChecker()

def correct_spelling(text):
    # Tokenize the input text
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors='pt'
    )

    # Generate a corrected text using RAG
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=512,
        num_beams=4,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    # Convert the generated IDs to text
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Use SpellCheck to correct any remaining spelling errors
    words = corrected_text.split()
    misspelled = spell.unknown(words)
    for word in misspelled:
        corrected_word = spell.correction(word)
        corrected_text = corrected_text.replace(word, corrected_word)

    # Use TextBlob to correct any grammatical errors
    blob = TextBlob(corrected_text)
    corrected_text = str(blob.correct())

    return corrected_text

# Test the function
texts = [
    "THIS IS A HANDWRITTER TEXT RECOGNISIOR ANT",
    "PIPELING THAT OPERATES ON SCANNED PAGES",
    "AND APPLIES THE FOLLOWING OPERATIONS",
    "SELECT WORDS",
    "READ WORDS"
]

for text in texts:
    print("Original Text:", text)
    print("Corrected Text:", correct_spelling(text))
    print("\n")