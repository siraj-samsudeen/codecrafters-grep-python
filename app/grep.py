def tokenize(pattern):
    special_chars = '\\['
    tokens = []

    token = char_needed = ''
    len_needed = -1

    def reset():
        nonlocal token, len_needed, char_needed
        token = char_needed = ''
        len_needed = -1

    def flush():
        if token:
            tokens.append(token)
        reset()
    
    for char in pattern:
        if char in special_chars:
            flush()
        if char == '\\':
            len_needed = 2
        elif char == '[':
            char_needed=']'

        token += char
        if len(token) == len_needed or char == char_needed:
            flush()
        # print(char, repr(token), tokens)
    flush()
    return tokens

def match_pattern(input_line, pattern):
    tokens = tokenize(pattern)
    # print("*" * 10, "matching ", repr(pattern), " to ", input_line, " tokens= ", tokens)
    i = j = 0

    def process_match(success):
        nonlocal i, j
        if success:
            # if there is a match, move to the next token
            # in case of match, we want to test the next char with next token
            j += 1
        else:
            # in case of no match, we want to retry the tokens from the beginning again
            j = 0

        # whether there is a match or not, we move to the next char
        i += 1


    while i < len(input_line) and j < len(tokens):
        # print(repr(input_line[i]), repr(tokens[j]))
        token = tokens[j]
        if token == '\\d':
            process_match(input_line[i].isdigit())
        elif token == '\\w':
            process_match(input_line[i].isalpha())
        elif token.startswith('[') and token.endswith(']'):
            token = token.strip('[]')
            # handle negative char groups first
            if token[0] == '^':
                token = token[1:]
                process_match(input_line[i] not in token)
            else:
                process_match(input_line[i] in token)
        else: # literal match
            text = input_line[i: i+len(token)]
            process_match(text == token)
    
    # if we exited the loop when all token are matched, then j would match the len of tokens
    return j == len(tokens)