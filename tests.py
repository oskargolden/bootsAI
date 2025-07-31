# tests.py

from functions.get_files_info import get_files_info

# Test 1: List current directory
result1 = get_files_info(".", ".")
print("Result for current directory:")
print(result1)

# Test 2: List pkg directory  
result2 = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
print(result2)

# Test 3: Try to access /bin (should fail)
result3 = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(result3)

# Test 4: Try to access ../ (should fail)
result4 = get_files_info("calculator", "../")
print("Result for '../' directory:")
print(result4)