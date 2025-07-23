import pandas as pd
import json
from collections import defaultdict, Counter
import re

def analyze_haiku(df):
    # Store words with their line context
    word_context = defaultdict(list)
    word_counts = Counter()
    
    for idx, row in df.iterrows():
        haiku_lines = [row['Line1'], row['Line2'], row['Line3']]
        
        # Verification step - check each word actually exists in the haiku
        full_text = ' '.join(haiku_lines).lower()
        
        
        for line_num, line in enumerate(haiku_lines, 1):
            # Clean but preserve meaningful words
            cleaned_line = re.sub(r'[^\w\s\']', '', line.lower())
            words = cleaned_line.split()
            
            # Custom stopwords that preserve meaningful words in haiku
            minimal_stopwords = {
                'the', 'and', 'or', 'but', 'nor', 'yet', 'so', 'of', 'is', 'in', 'a', 'an', 'to', 'for', 'at', 'by', 
                'with', 'on', 'am', 'are', 'was', 'were', 'be', 'been', 'as', 'than', 'that', 'who', 'what', 'where',
                'when', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
                'no', 'not', 'only', 'own', 'same', 'too', 'very', 'can', 'will', 'just', 'should', 'now', 'from',
                'into', 'over', 'again', 'once', 'under', 'further', 'before', 'after', 'above', 'below', 'up',
                'down', 'out', 'about', 'between', 'through', 'during', 'within', 'among', 'those', 'these', 'them'
            }
            
            for word in words:
                if word not in minimal_stopwords:
                    # Store the word with its context
                    # Only add words that actually appear in the text
                    if word in full_text:
                        word_context[word].append({
                        'haiku_id': idx,
                        'line_num': line_num,
                        'full_line': line
                    })
                    word_counts[word] += 1
    
    # Convert to D3-compatible format with context
    word_data = [
        {
            "text": word,
            "size": count,
            "occurrences": [
                {
                    "haiku_id": ctx['haiku_id'],
                    "line_num": ctx['line_num'],
                    "line_text": ctx['full_line']
                }
                for ctx in contexts
            ]
        }
        for word, contexts in word_context.items()
        for count in [word_counts[word]]
    ]
    
    return word_data

# Load and process the data
df = pd.read_csv("../data/haiku.csv")
word_data = analyze_haiku(df)

# Save to JSON
with open("../output/haiku_word_cloud.json", "w") as f:
    json.dump(word_data, f, indent=2)