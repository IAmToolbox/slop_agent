from functions.get_files_info import get_files_info

# Test 1
print(get_files_info("calculator"))

# Test 2
print(get_files_info("calculator", "pkg"))

# Test 3
print(get_files_info("calculator", "/bin"))

# Test 4
print(get_files_info("calculator", "../"))