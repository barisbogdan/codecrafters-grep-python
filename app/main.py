import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


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
    while input_line:
        if pattern[0] == "\\":
            if 1 < len(pattern):
                if pattern[1] == "d":
                    if not match_digit(input_line):
                        return False
                elif pattern[1] == "w":
                    if not match_alphanumeric(input_line):
                        return False
                else:
                    return False
                input_line = input_line[2:]
                pattern = pattern[2:]
            else:
                return False
        elif pattern[0] == "[":
            end_idx = pattern.find("]")
            group = pattern[1:end_idx]
            if group.startswith("^"):
                if not match_negative_group(input_line, group[1:]):
                    return False
            else:
                if not match_positive_group(input_line, group):
                    return False
            pattern = pattern[end_idx + 2:]
            input_line = input_line[end_idx + 2:]
        else:
            if not match_literal(input_line, pattern[0]):
                return False
            input_line = input_line[1:]
            pattern = pattern[1:]

    return True

def calculate_lenght(pattern):
    char = 0
    while pattern:
        if pattern[0] == "\\":
            if 1 < len(pattern):
                if pattern[1] == "d" or pattern[1] == "w":
                    pattern = pattern[2:]
                    char += 2
                else:
                    exit(1)
        elif pattern[0] == "[":
            end_idx = pattern.find("]")
            pattern = pattern[end_idx + 2:]
            char += 1
        else:
            pattern = pattern[1:]
            char += 1
    return char

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    pattern_lenght = calculate_lenght(pattern)
    iteration = 0
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    while iteration + pattern_lenght <= len(input_line):
        if match_pattern(input_line[iteration:iteration + pattern_lenght], pattern):
            exit(0)
        iteration += 1
    
    exit(1)


if __name__ == "__main__":
    main()
