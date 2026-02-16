from functions.get_files_info import get_files_info

print("1. ")
print(get_files_info("calculator", "."))
print("2. ")
print(get_files_info("calculator", "pkg"))
print("3. ")
print(get_files_info("calculator", "/bin"))
print("4. ")
print(get_files_info("calculator", "../"))

