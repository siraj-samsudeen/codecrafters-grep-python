def tokenize(pattern):
    special_chars = '\\[.|('
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
        if len(token) == len_needed or char == char_needed or char in '.)':
            flush()
        
        if char in '+?':
            if len(token) > 2: 
                token, extra = token[:-2], token[-2:]
                flush(extra)
            else:
                flush()
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
    i = j = 0

    alternation_on = False

    def process_match(success, match_length=1):
        nonlocal i, j, matchFailed
        if success:
            # if there is a match, move to the next token
            # in case of match, we want to test the next char with next token
            j += 1
            matchFailed = False
        else:
            # in case of alternation, we want to move to the next token
            if alternation_on:
                match_length = 0
                j += 1
            else:
                # in case of no match, we want to retry the tokens from the beginning again
                j = 0
            matchFailed = True

        # whether there is a match or not, we move to the next char
        i += match_length

    while i < len(input_line) and j < len(tokens):
        token = tokens[j]

        if token.startswith('('):
            alternation_on = True
            token = token[1:]
        if token.endswith(')'):
            alternation_on = False
            token = token[:-1]
        
        if token.startswith('|'):
            token = token[1:]

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
        elif token[-1] == '+':
            quantifier = token[-1]
            token = token[:-1]
            temp = i
            while token == input_line[temp]:
                temp += 1
            process_match(temp > i, (temp-i) or 1)
        elif token[-1] == '?':
            quantifier = token[-1]
            token = token[:-1]
            if token == input_line[i]:
                process_match(True, 1)
            else:
                process_match(True, 0)
        elif token == '.':
                process_match(True, 1)
        else: # literal match
            text = input_line[i: i+len(token)]
            process_match(text == token, len(token))
        
        if matchStart and matchFailed:
            return False
    
    # if we exited the loop when all token are matched, then j would match the len of tokens
    # if there are optional quantifiers at the end, mark them as True
    while j < len(tokens):
        # if alternation is On and we are still left with alternatives, we can pass
        # but we can't have other type of tokens
        if alternation_on and not matchFailed and tokens[j].startswith("|"):
            j +=1
        else:
            break
    while j < len(tokens):
        if '?' in tokens[j]:
            j +=1
        else:
            break
    if matchEnd:
        return i == len(input_line)
    else:
        return j == len(tokens)