import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

from test_grep import match_pattern
# def match_pattern(input_line, pattern):
#     if len(pattern) == 1:
#         return pattern in input_line
#     elif pattern == '\d':
#         for char in input_line:
#             is_digit = ord('0') < ord(char) < ord('9')
#             is_digit = '0' < char < '9'
#             if is_digit:
#                 return True
#             return False
#     elif pattern == '\w':
#         for char in input_line:
#             is_digit = ord('0') < ord(char) < ord('9')
#             is_lower_case = ord('a') < ord(char) < ord('z')
#             is_upper_case = ord('A') < ord(char) < ord('Z')
#             if is_digit or is_lower_case or is_upper_case:
#                 return True
#         return False
#     # this has to come before the positive char groups
#     elif pattern.startswith("[^") and pattern.endswith("]"):
#         str_to_match = pattern.strip("[^]")
#         return not any(c in str_to_match for c in input_line)
#     elif pattern.startswith("[") and pattern.endswith("]"):
#         str_to_match = pattern[1:-1]
#         for char in input_line:
#             if char in str_to_match:
#                 return True
#         return False
#     else:
#         raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
