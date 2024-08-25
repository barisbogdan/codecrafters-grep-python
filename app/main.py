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

def match_quantifier(input_line, pattern):
    char_to_match = pattern[0]
    remaining_pattern = pattern[2:]
    stack = []
    loop = True
    while loop:
        if match_literal(input_line[0], char_to_match):
            input_line = input_line[1:]
            stack = [input_line, remaining_pattern] + stack
        else:
            loop = False
    if stack:
        return stack
    else:
        return False

def match_pattern(pattern_stack):
    while pattern_stack:
        code = True
        input_line = pattern_stack[0]
        pattern = pattern_stack[1]
        pattern_stack = pattern_stack[2:]
        while pattern:
            if len(pattern) > 1 and pattern[1] == "+":
                stack = match_quantifier(input_line, pattern)
                if stack:
                    pattern_stack = stack + pattern_stack
                    del stack
                code = False
            elif len(pattern) > 1 and pattern[1] == "?":
                if match_literal(input_line, pattern[0]):
                    input_line = input_line[1:]
                pattern = pattern[2:]
            elif pattern[0] == "\\":
                if 1 < len(pattern):
                    if pattern[1] == "d":
                        if not match_digit(input_line[0]):
                            code = False
                    elif pattern[1] == "w":
                        if not match_alphanumeric(input_line[0]):
                            code = False
                    else:
                        code = False
                    input_line = input_line[1:]
                    pattern = pattern[2:]
                else:
                    code = False
            elif pattern[0] == "[":
                end_idx = pattern.find("]")
                group = pattern[1:end_idx]
                if group.startswith("^"):
                    if not match_negative_group(input_line[0], group[1:]):
                        code = False
                else:
                    if not match_positive_group(input_line[0], group):
                        code = False
                pattern = pattern[end_idx + 2:]
                input_line = input_line[1:]
            else:
                if not match_literal(input_line[0], pattern[0]):
                    code = False
                input_line = input_line[1:]
                pattern = pattern[1:]

            if not code:
                pattern = ""

        if code:
            return True

    return False

def generate_combinations(input_line, pattern, pattern_length):
    combinations = []

    if pattern.startswith("^"):
        for i in range(pattern_length[1], pattern_length[0] - 1, -1):
            combinations.append([input_line[:i], pattern[1:]])
    elif pattern[::-1].startswith("$"):
        pattern = pattern[::-1]
        input_line = input_line[::-1]
        for i in range(pattern_length[1], pattern_length[0] - 1, -1):
            combinations.append([input_line[:i], pattern[1:]])
    else:
        for i in range(pattern_length[1], pattern_length[0] - 1, -1):
            for j in range(len(input_line) - i + 1):
                combinations.append([input_line[j:j+i], pattern])

    return combinations
    
def calculate_length(pattern, input_line):
    min_char = 0
    max_char = 0
    while pattern:
        if pattern[0] == "+":
            max_char = len(input_line)
            pattern = pattern[1:]
        elif pattern[0] == "?":
            min_char -= 1
            pattern = pattern[1:]
        elif pattern[0] == "\\":
            if 1 < len(pattern):
                if pattern[1] == "d" or pattern[1] == "w":
                    pattern = pattern[2:]
                    min_char += 1
                    if max_char <= len(input_line):
                        max_char += 1
                else:
                    exit(1)
        elif pattern[0] == "[":
            end_idx = pattern.find("]")
            pattern = pattern[end_idx + 2:]
            min_char += 1
            if max_char <= len(input_line):
                max_char += 1
        else:
            pattern = pattern[1:]
            min_char += 1
            if max_char <= len(input_line):
                max_char += 1
    return [min_char, max_char]

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    pattern_to_calculate = pattern
    if pattern_to_calculate.startswith("^"):
        pattern_to_calculate = pattern_to_calculate[1:]
    if pattern_to_calculate[::-1].startswith("$"):
        pattern_to_calculate = pattern_to_calculate[:-1]
    pattern_lenght = calculate_length(pattern_to_calculate, input_line)
    del pattern_to_calculate
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    combinations = generate_combinations(input_line, pattern, pattern_lenght)
    while combinations:
        if match_pattern(combinations[0]):
            exit(0)
        combinations = combinations[1:]
    
    exit(1)


if __name__ == "__main__":
    main()
