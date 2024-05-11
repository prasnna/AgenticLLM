import os
import re
import csv

def extract_keywords_from_java_code(java_code):
    keywords = set()

    # Regular expression patterns to match class names, field names, and method names
    class_pattern = r'class\s+(\w+)\s*\{'
    field_pattern = r'\bprivate\s+\w+\s+(\w+)\s*;'
    method_pattern = r'\b(\w+)\s+\w+\s*\([^\)]*\)\s*\{'

    # Extract class names
    class_names = re.findall(class_pattern, java_code)
    keywords.update(class_names)

    # Extract field names
    field_names = re.findall(field_pattern, java_code)
    keywords.update(field_names)

    # Extract method names
    method_names = re.findall(method_pattern, java_code)
    keywords.update(method_names)

    return keywords

def process_java_files_in_directory(directory):
    all_keywords = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    java_code = f.read()
                    keywords = extract_keywords_from_java_code(java_code)
                    all_keywords.update(keywords)
    return all_keywords

def write_keywords_to_csv(keywords, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Keyword'])
        for keyword in keywords:
            writer.writerow([keyword])

# Directory containing Java files
java_directory = '\\Desktop\\AgenticLLM\\AgenticLLM\\sql-scripts\\'

# Process Java files and extract keywords
all_keywords = process_java_files_in_directory(java_directory)

# Write keywords to CSV file
output_csv_file = 'java_keywords.csv'
write_keywords_to_csv(all_keywords, output_csv_file)