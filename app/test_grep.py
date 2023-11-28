import pytest
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
    assert tokenize('a+ apple') == ['a+', ' apple']
    assert tokenize('a+apple') == ['a+', 'apple']
    assert tokenize('apple+') == ['appl','e+']
    assert tokenize('ca+t') == ['c','a+', 't']
    assert tokenize('dogs?') == ['dog','s?']
    assert tokenize('ca?t') == ['c','a?', 't']
    assert tokenize('d.g') == ['d','.','g']
    assert tokenize('(cat|dog)') == ['(cat','|dog)']
    assert tokenize('(cat|dog|hello)') == ['(cat','|dog', '|hello)']
    assert tokenize('a (cat|dog)') == ['a ', '(cat','|dog)']
    assert tokenize('a (cat|dog) and') == ['a ', '(cat','|dog)', ' and']

# @pytest.mark.skip("hi")
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

    assert match_pattern('dog', 'dog$')
    assert not match_pattern('dogs', 'dog$')

    assert match_pattern( 'apple','a+')
    assert match_pattern( 'SaaS','a+')
    assert not match_pattern( 'dog','a+')
    assert match_pattern( 'caaats','ca+t')

    assert match_pattern( 'doga','dogs?')
    assert match_pattern( 'dog','dogs?')
    
    assert match_pattern( 'act','ca?t')
    assert match_pattern( 'dog','d.g')
    assert match_pattern( 'dog','(cat|dog)')
    assert match_pattern( 'dog','(dog|cat)')
    assert match_pattern( 'a cat','a (cat|dog)')