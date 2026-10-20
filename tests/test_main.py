import pytest 
from main import(is_palindrome, fibonacci, count_vowels, calculate_discount, flatten_list, word_frequencies, is_prime)

def test_is_palindrome():
    assert is_palindrome("kajak") == True
    assert is_palindrome("Kobyła ma mały bok") == True
    assert is_palindrome("Hello") == False
    assert is_palindrome("") == True    
    assert is_palindrome("A") == True

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    with pytest.raises(ValueError):
        fibonacci(-1)

def test_count_vowels():
    assert count_vowels("Hello World") == 3
    assert count_vowels("Python") == 2
    assert count_vowels("AEIOUY") == 6
    assert count_vowels("Próba żółwia") == 3
    assert count_vowels("bcd") == 0
    assert count_vowels("") == 0

def test_calculate_discount():
    assert calculate_discount(100, 0.2) == 80.0
    assert calculate_discount(50, 0.5) == 25.0
    with pytest.raises(ValueError):
        calculate_discount(100, -0.1)
    with pytest.raises(ValueError):
        calculate_discount(100, 1.5)

def test_flatten_list():
    assert flatten_list([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
    assert flatten_list([[1], [2], [3]]) == [1, 2, 3]
    assert flatten_list([]) == []

def test_word_frequencies():
    assert word_frequencies("Hello, hello! How are you?") == {'hello': 2, 'how': 1, 'are': 1, 'you': 1}
    assert word_frequencies("Python is great. Python is fun!") == {'python': 2, 'is': 2, 'great': 1, 'fun': 1}
    assert word_frequencies("") == {}

def test_is_prime():
    assert is_prime(0) == False
    assert is_prime(1) == False
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(5) == True
    assert is_prime(6) == False
    assert is_prime(7) == True
    assert is_prime(8) == False
    assert is_prime(9) == False
    assert is_prime(10) == False
    assert is_prime(97) == True

