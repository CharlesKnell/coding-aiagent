from functions.write_file import write_file

print("1. ", end="")
print(write_file("calculator/pkg/newdir", "write_test1.py", "the quick brown fox"))
print("2. ", end="")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("3. ", end="")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("4. ", end="")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
 