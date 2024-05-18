import os
import shutil
from dotenv import load_dotenv

load_dotenv()

folder_path = os.environ['repo_path']


def is_code_file(file_name):
    code_extensions = ('.java')  # Add more extensions as needed
    return file_name.endswith(code_extensions)

def collect_code_files(folder_path, output_file):
    with open(output_file, 'wb') as out_file:
        for folder_name, _, file_names in os.walk(folder_path):
            for file_name in file_names:
                if is_code_file(file_name):
                    file_path = os.path.join(folder_name, file_name)
                    with open(file_path, 'rb') as in_file:
                        shutil.copyfileobj(in_file, out_file)
                        out_file.write(b'\n')  # add a newline between files
                        out_file.write(b'-' * 50)  # add a line separator between files
                        out_file.write(b'\n')  # add a newline after the line separator


output_file = 'code_files_1.txt'
collect_code_files(folder_path, output_file)
print("Code files collected and merged successfully into", output_file)


# import os
# import shutil



# def collect_code_files(folder_path, output_file):
#     with open(output_file, 'wb') as out_file:
#         for folder_name, _, file_names in os.walk(folder_path):
#             for file_name in file_names:
#                     file_path = os.path.join(folder_name, file_name)
#                     with open(file_path, 'rb') as in_file:
#                         shutil.copyfileobj(in_file, out_file)
#                         out_file.write(b'\n')  # add a newline between files
#                         out_file.write(b'-' * 50)  # add a line separator between files
#                         out_file.write(b'\n')  # add a newline after the line separator

# # Example usage
# output_file = 'code_files.txt'
# collect_code_files(folder_path, output_file)
# print("Code files collected and merged successfully into", output_file)
