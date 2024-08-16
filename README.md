# NERRULE-Password-Strength
**Password Analyzer System**
**Introduction**

This project is focused on creating a Password Analyzer system that enhances password security by combining machine learning with rule-based algorithms. The system is designed to evaluate the strength of passwords based on established criteria and to identify potential security risks by detecting personal information within the password.

**Key Features**
Machine Learning Integration: The system uses a pre-trained BERT model for Named Entity Recognition (NER). This model is capable of identifying entities such as names, dates, and locations within the password, which may compromise security.

Rule-Based Password Strength Assessment: The system assesses the strength of a password based on specific criteria, including:

Length (must be at least 8 characters)
Presence of digits
Use of both uppercase and lowercase letters
Inclusion of special characters
Dynamic Password Strength Scoring: If the password contains any named entities, the overall strength score is reduced. This reflects the potential vulnerability of using easily identifiable personal information in passwords.

How It Works
1. NER Pipeline Initialization
The system begins by importing necessary modules and initializing the NER pipeline using the dslim/bert-base-NER model. This machine learning model is specifically trained for token classification tasks, allowing it to identify named entities within text.

**python
Copy code**
_from transformers import pipeline
import re_

_ner_pipe = pipeline("token-classification", model="dslim/bert-base-NER")_
2. Assessing Password Strength
The assess_password_strength function evaluates the password against five key criteria. Each criterion, such as having at least one digit or one special character, contributes to the overall strength score. The password strength is then calculated as a percentage of the total criteria met.

**python
Copy code**
def assess_password_strength(password):
    criteria = {
        'length': len(password) >= 8,
        'digit': re.search(r'\d', password) is not None,
        'uppercase': re.search(r'[A-Z]', password) is not None,
        'lowercase': re.search(r'[a-z]', password) is not None,
        'special_char': re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None
    }
    
    met_criteria = sum(criteria.values())
    total_criteria = len(criteria)
    strength_percentage = (met_criteria / total_criteria) * 100
    
    return strength_percentage
3. Checking for Named Entities
The contains_named_entities function utilizes the NER pipeline to scan the password for any named entities. If such entities are found, it suggests that the password may contain personal information, making it less secure.

**python
Copy code**
def contains_named_entities(password):
    results = ner_pipe(password)
    for result in results:
        if result['entity'] in ['B-PER', 'B-DATE', 'B-LOC']:
            return True
    return False
4. Adjusting Password Strength
After evaluating the password's strength and checking for named entities, the system adjusts the password strength score accordingly. If named entities are detected, the system reduces the password strength by 20% to reflect the increased risk.

**python
Copy code**
password_strength_percentage = assess_password_strength(password)
entity_in_password = contains_named_entities(password)

if entity_in_password:
    password_strength_percentage -= 20
    if password_strength_percentage < 0:
        password_strength_percentage = 0
5. Example Analysis
An example password is analyzed using the system. The named entities identified, along with their respective labels and confidence scores, are printed, followed by the final calculated password strength.

**python
Copy code**
password = "./2qwerE*"

for result in ner_pipe(password):
    print(f"Entity: {result['word']}, Label: {result['entity']}, Score: {result['score']:.4f}")

print(f"\nPassword Strength: {password_strength_percentage:.2f}%")
