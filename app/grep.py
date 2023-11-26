def tokenize(pattern):
    special_chars = '\\['
    tokens = []

    token = char_needed = ''
    len_needed = -1

    def reset():
        nonlocal token, len_needed, char_needed
        token = char_needed = ''
        len_needed = -1

    def flush(extra=None):
        if token:
            tokens.append(token)
        if extra:
            tokens.append(extra)
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
        
        if char in ['+']:
            if len(token) > 2: 
                token, extra = token[:-2], token[-2:]
                flush(extra)
                print(token, extra)
            else:
                flush()
        # print(char, repr(token), tokens)
    flush()
    return tokens

def match_pattern(input_line, pattern):
    matchStart = False
    matchEnd = False
    matchFailed = False
    if pattern.startswith('^'):
        matchStart = True
        pattern = pattern[1:]
    if pattern.endswith('$'):
        matchEnd = True
        pattern = pattern[:-1]

    tokens = tokenize(pattern)
    print("*" * 10, "matching ", repr(pattern), " to ", input_line, " tokens= ", tokens)
    i = j = 0

    def process_match(success, match_length=1):
        nonlocal i, j, matchFailed
        if success:
            # if there is a match, move to the next token
            # in case of match, we want to test the next char with next token
            j += 1
        else:
            # in case of no match, we want to retry the tokens from the beginning again
            j = 0
            matchFailed = True

        # whether there is a match or not, we move to the next char
        i += match_length


    while i < len(input_line) and j < len(tokens):
        # print(repr(input_line[i]), repr(tokens[j]), matchFailed)
        token = tokens[j]
        repeat_plus = False
        if token.endswith('+'):
            repeat_plus = True
            token = token[:-1]

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
            if repeat_plus:
                temp = i
                while token == input_line[temp]:
                    temp += 1
                # print(f"found {temp-i}  matches for {token} in {input_line}")
                process_match(temp > i, (temp-i) or 1)
            else:
                text = input_line[i: i+len(token)]
                process_match(text == token, len(token))
        
        if matchStart and matchFailed:
            return False
    
    # if we exited the loop when all token are matched, then j would match the len of tokens
    if matchEnd:
        # print(i, j)
        return i == len(input_line)
    else:
        return j == len(tokens)