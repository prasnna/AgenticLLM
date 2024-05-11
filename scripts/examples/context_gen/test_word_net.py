from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def generate_real_world_tokens(sql_query):
    tokens = sql_query.split()
    real_world_tokens = []
    for token in tokens:
        synonyms = get_synonyms(token)
        if synonyms:
            real_world_tokens.extend(synonyms)
        else:
            real_world_tokens.append(token)
    return real_world_tokens

# Example SQL query
sql_query = "query"

# Generate real-world tokens
real_world_tokens = generate_real_world_tokens(sql_query)
print(real_world_tokens)
