from functions.get_files_info import run_python_file

# should print the calculator's usage instructions
result1 = run_python_file("calculator", "main.py")
print(result1)

# should run the calculator... which gives a kinda nasty rendered result
result2 = run_python_file("calculator", "main.py", ["3 + 5"])
print(result2)

# 
result3 = run_python_file("calculator", "tests.py")
print(result3)

# this should return an error
result4 = run_python_file("calculator", "../main.py")
print(result4)

# this should return an error
result5 = run_python_file("calculator", "nonexistent.py")
print(result5)





