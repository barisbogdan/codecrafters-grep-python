import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if pattern[0] == "\\":
        if pattern == "\d":
            for letter in input_line:
                if letter.isdigit():
                    exit(0)
        if pattern == "\w":
            for letter in input_line:
                if letter.isalnum() or letter == "_":
                    exit(0)
        exit(1)

    if pattern[0] == "[" and pattern[-1] == "]":
        pattern = pattern[1:-1]
        if pattern[0] == "^":
            pattern = pattern[1:]
            for letter in pattern:
                if match_pattern(input_line, letter):
                    exit(1)
            exit(0)
        else:    
            for letter in pattern:
                if match_pattern(input_line, letter):
                    exit(0)
            exit(1)


    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
