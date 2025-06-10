
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def test_get_files_info():

    result1 = get_files_info("calculator", ".")
    print(result1)

    result2 = get_files_info("calculator", "pkg")
    print(result2)

    result3 = get_files_info("calculator", "/bin")
    print(result3)

    result4 = get_files_info("calculator", "../")
    print(result4)

def test_get_file_content():

    # result1 = get_file_content("calculator", "lorem.txt")
    # print(result1)

    result2 = get_file_content("calculator", "main.py")
    print(result2)

    result3 = get_file_content("calculator", "pkg/calculator.py")
    print(result3)

    result4 = get_file_content("calculator", "/bin/cat")
    print(result4)


test_get_file_content()