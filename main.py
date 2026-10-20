def is_palindrome(text: str) -> bool:
    """Sprawdza, czy tekst jest palindromem (ignoruje wielkość liter i spacje)."""
    tekst = text.lower().replace(" ", "")
    dlugosc = len(tekst)
    for i in range(dlugosc):
        if tekst[i] != tekst[dlugosc - 1 - i]:
            return False
    return True


def fibonacci(n: int) -> int:
    """Zwraca n-ty element ciągu Fibonacciego. Dla n < 0 zgłasza ValueError."""
    if n < 0:
        raise ValueError("n musi być nieujemne")
    a = 0
    b = 1
    for i in range(n):
        nastepna = a + b
        a = b
        b = nastepna
    return a


def count_vowels(text: str) -> int:
    """Zlicza samogłoski (a, e, i, o, u, y), bez względu na wielkość liter."""
    samogloski = "aeiouy"
    licznik = 0
    for znak in text.lower():
        if znak in samogloski:
            licznik += 1
    return licznik


def calculate_discount(price: float, discount: float) -> float:
    """Zwraca cenę po zniżce. Zniżka musi być w zakresie 0-1, inaczej ValueError."""
    if discount < 0 or discount > 1:
        raise ValueError("zniżka musi być w zakresie od 0 do 1")
    return float(price * (1 - discount))


def flatten_list(nested_list: list) -> list:
    """Spłaszcza listę z zagnieżdżonymi listami."""
    wynik = []
    for element in nested_list:
        if isinstance(element, list):
            for x in flatten_list(element):
                wynik.append(x)
        else:
            wynik.append(element)
    return wynik


def word_frequencies(text: str) -> dict:
    """Zwraca słownik z częstością słów (ignoruje wielkość liter i interpunkcję)."""
    # zamieniamy wszystko, co nie jest literą ani cyfrą, na spację
    czysty = ""
    for znak in text.lower():
        if znak.isalnum():
            czysty += znak
        else:
            czysty += " "

    wynik = {}
    for slowo in czysty.split():
        if slowo in wynik:
            wynik[slowo] += 1
        else:
            wynik[slowo] = 1
    return wynik


def is_prime(n: int) -> bool:
    """Sprawdza, czy liczba jest pierwsza. Dla n < 2 zwraca False."""
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True