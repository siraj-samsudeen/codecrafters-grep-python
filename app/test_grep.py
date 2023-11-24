from grep import tokenize, match_pattern

def test_tokenizer():
    assert tokenize(r'\d apple') == ['\\d', ' apple']
    assert tokenize(r'apple\d ') == ['apple', '\\d', ' ']
    assert tokenize(r'\wapple \d ') == ['\\w','apple ', '\\d', ' ']
    assert tokenize(r'\d\d\d apple') == ['\\d','\\d','\\d',' apple']
    assert tokenize(r'\d \w\w\ws') == ['\\d',' ', '\\w','\\w','\\w','s']
    assert tokenize('[abcd]') == ['[abcd]']
    assert tokenize('ab[abcd]') == ['ab', '[abcd]']
    assert tokenize('[abcd]ab') == ['[abcd]', 'ab']


def test_match_pattern():
    assert match_pattern('dog', 'd')
    assert not match_pattern('dog', 'f')
    assert match_pattern('123', r'\d')
    assert not match_pattern('apple', r'\d')

    assert match_pattern('word', r'\w')
    assert not match_pattern('$!?', r'\w')

    assert match_pattern('a', '[abcd]')
    assert not match_pattern('dog', '[abc]')
    assert match_pattern('dog', '[^abc]')
    assert not match_pattern('cab', '[^abc]')

    assert match_pattern('1 apple', r'\d apple')
    assert not match_pattern('1 orange', r'\d apple') 
    assert match_pattern('100 apple', r'\d\d\d apple')
    assert not match_pattern('1 apple', r'\d\d\d apple') 
    assert match_pattern('3 dogs', r'\d \w\w\ws') 
    assert match_pattern('4 cats', r'\d \w\w\ws') 
    assert not match_pattern('1 dog', r'\d \w\w\ws') 

    assert match_pattern('log', '^log')
    assert not match_pattern('slog', '^log')

