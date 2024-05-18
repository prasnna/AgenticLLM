import ast

string_data = "{'TABLE_NAME': 'TBL_SUPP_CONTRACT_CONVERSION_20220816_MN'}, {'TABLE_NAME': 'TBL_SUPP_CONTRACT_CONVERSION_20220816_MN'}, {'TABLE_NAME': 'TBL_SUPP_CONTRACT_CONVERSION_20220908'}, {'TABLE_NAME': 'TBL_SUPP_CONTRACT_CONVERSION_20220908'}, {'TABLE_NAME': 'TBL_SUPP_CONTRACT_CONVERSION'}, {'TABLE_NAME': 'TBL_SUPP_CONTRACT_CONVERSION'}"

# Remove the leading and trailing '[' and ']' characters
cleaned_string = string_data.lstrip('[').rstrip(']')

# Convert the string to a list of dictionaries
list_of_dicts = [ast.literal_eval(item) for item in cleaned_string.split(', ')]

print(list_of_dicts)