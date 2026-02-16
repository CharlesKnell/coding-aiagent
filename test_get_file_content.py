from functions.get_file_content import get_file_content

print("1. ")
print(get_file_content("calculator", "main.py"))
print("2. ")
print(get_file_content("calculator", "pkg/calculator.py"))
print("3. ")
print(get_file_content("calculator", "bin/cat"))
print("4. ")
print(get_file_content("calculator", "pkg/does_not_exist.py"))

