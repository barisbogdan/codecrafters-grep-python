import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!
# only these packages available for this challenge

def match_literal(input_line, char):
    return char in input_line

def match_digit(input_line):
    return any(char.isdigit() for char in input_line)

def match_alphanumeric(input_line):
    return any(char.isalnum() or char == "_" for char in input_line)

def match_positive_group(input_line, group):
    return any(char in input_line for char in group)

def match_negative_group(input_line, group):
    return not any(char in input_line for char in group)

def match_pattern(input_line, pattern):
    if not pattern:
        exit(1)
    
    i = 0
    while i < len(pattern):
        if pattern[i] == "\\":
            if i + 1 < len(pattern):
                if pattern[i + 1] == "d":
                    if not match_digit(input_line):
                        exit(1)
                elif pattern[i + 1] == "w":
                    if not match_alphanumeric(input_line):
                        exit(1)
                else:
                    exit(1)
                i += 2
            else:
                exit(1)
        elif pattern[i] == "[":
            end_idx = pattern.find("]", i)
            group = pattern[i + 1:end_idx]
            if group.startswith("^"):
                if not match_negative_group(input_line, group[1:]):
                    exit(1)
            else:
                if not match_positive_group(input_line, group):
                    exit(1)
            i = end_idx + 1
        else:
            if not match_literal(input_line, pattern[i]):
                exit(1)
            i += 1

    exit(0)


def main():
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
