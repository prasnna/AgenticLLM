from config import url

import pandas as pd
from sqlalchemy import create_engine
from nltk.corpus import wordnet
from sqlalchemy.engine import reflection

def apply_rules(forms, rules):
    return [
        form
        for form in forms
        for rule in rules
        if form.endswith(rule.encode("utf-8"))  # Convert rule to bytes
    ]

wordnet.apply_rules = apply_rules


# Define the connection string
connection_string = f'mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0'

engine = create_engine(connection_string)
connection = engine.connect()

inspector = reflection.Inspector.from_engine(engine)
tables = inspector.get_table_names()

# Define the generate_description function
def generate_description(df):
    # Data profiling
    num_rows, num_cols = df.shape
    data_types = df.dtypes.astype(str).tolist()
    unique_values = [df[column].nunique() for column in df.columns]

    # Entity recognition (simple example)
    entities = []
    for column in df.columns:
        if df[column].dtype == 'object':
            entities.extend(df[column].tolist())

    # WordNet integration
    wordnet_descriptions = []
    for entity in entities:
        if entity is not None:
            synsets = wordnet.synsets(entity)
            if synsets:
                wordnet_descriptions.append(synsets[0].definition())
            else:
                wordnet_descriptions.append("No WordNet description found")
        else:
            wordnet_descriptions.append("No entity found")

    # Generate description
    description = f"This table has {num_rows} rows and {num_cols} columns. "
    description += f"The data types are: {', '.join(data_types)}. "
    description += f"The number of unique values in each column are: {', '.join(map(str, unique_values))}. "
    description += f"Entities found: {', '.join(entities)}. "
    description += f"WordNet descriptions: {', '.join(wordnet_descriptions)}."

    return description

# Iterate through each table
for table in tables:
  if not table.startswith("ADT_"):
    # Read a few rows
    df = pd.read_sql_query(f"SELECT TOP 5 * FROM {table}", connection)

    # Generate natural language description
    description = generate_description(df)

    # Print or store the description
    print(f"{table} description: {description}")