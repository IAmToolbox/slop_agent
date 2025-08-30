from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

# Test 1
print(get_file_content("calculator", "main.py"))

# Test 2
print(get_file_content("calculator", "pkg/calculator.py"))

# Test 3
print(get_file_content("calculator", "/bin/cat"))

# Test 4
print(get_file_content("calculator", "pkg/does_not_exist.py"))