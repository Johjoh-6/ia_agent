# from subdirectory.filename import function_name
# import unittest
from functions.get_files_content import get_file_content
from functions.run_python_file import run_python_file
# from functions.get_files_info import get_files_info

# result = get_files_info("calculator", ".")
# print(result)
# result = get_files_info("calculator", "pkg")
# print(result)
# result = get_files_info("calculator", "/bin")
# print(result)
# result = get_files_info("calculator", "/bin")
# print(result)
# result = get_file_content("calculator", "lorem.txt")
# print(result)
# result = get_file_content("calculator", "main.py")
# print(result)
# result = get_file_content("calculator", "pkg/calculator.py")
# print(result)
# result = get_file_content("calculator", "/bin/cat")
# print(result)
# from functions.write_file import write_file

# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
# class TestGetFilesInfo(unittest.TestCase):
#     def test_get_files_info(self):
#         result = get_files_info("calculator", ".")
#         self.assertIsInstance(result, list)
#         print(result)

#     def test_get_files_info_with_pkg(self):
#         result = get_files_info("calculator", "pkg")
#         self.assertIsInstance(result, list)
#         print(result)

#     def test_get_files_info_with_bin(self):
#             result = get_files_info("calculator", "/bin")
#             # should return a list with a single string starting with Error
#             self.assertIsInstance(result, list)
#             self.assertTrue(len(result) == 1)
#             self.assertTrue(isinstance(result[0], str))
#             self.assertTrue(result[0].startswith("Error"))
#             print(result)

#     def test_get_files_info_with_parent(self):
#         result = get_files_info("calculator", "../")
#         print(result)
#         self.assertIsInstance(result, list)
#         self.assertTrue(len(result) == 1)
#         self.assertTrue(isinstance(result[0], str))
#         self.assertTrue(result[0].startswith("Error"))
