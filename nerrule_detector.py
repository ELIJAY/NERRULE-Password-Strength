from transformers import pipeline
import re

ner_pipe = pipeline("token-classification", model="dslim/bert-base-NER") #Machine learning Algorithm used

def assess_password_strength(password):
    criteria = {
        'length': len(password) >= 8,
        'digit': re.search(r'\d', password) is not None,
        'uppercase': re.search(r'[A-Z]', password) is not None,
        'lowercase': re.search(r'[a-z]', password) is not None,
        'special_char': re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None #Rule - based Algorithm of length, lower and uppercase alphabet, numbers and symbols 
    }
    
    met_criteria = sum(criteria.values())
    total_criteria = len(criteria)
    strength_percentage = (met_criteria / total_criteria) * 100
    
    return strength_percentage

def contains_named_entities(password):
    results = ner_pipe(password)
    for result in results:
        if result['entity'] in ['B-PER', 'B-DATE', 'B-LOC']:
            return True
    return False

password = "./2qwerE*" #No numbers, and uppercase

password_strength_percentage = assess_password_strength(password)
entity_in_password = contains_named_entities(password)

if entity_in_password:
    password_strength_percentage -= 20
    if password_strength_percentage < 0:
        password_strength_percentage = 0


for result in ner_pipe(password):
    print(f"Entity: {result['word']}, Label: {result['entity']}, Score: {result['score']:.4f}")

print(f"\nPassword Strength: {password_strength_percentage:.2f}%")
