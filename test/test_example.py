import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2

def test_is_instance():
    assert isinstance(1, int)
    assert isinstance(1.0, float)
    assert isinstance('1', str)

def test_boolean():
    validate = True
    assert validate is True
    assert ('hello' == 'world') is False

def test_type():
    assert type(1 is int)
    assert type(1.0 is float)
    assert type('1' is not int)

def test_greater_than_or_less_than():
    assert 1 > 0
    assert 4 < 10

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'Computer Science', 2)

def test_person_initialization(default_student):
    p = default_student
    assert p.first_name == 'John', 'First name should be John'
    assert p.last_name == 'Doe', 'Last name should be Doe'
    assert p.major == 'Computer Science', 'Major should be Computer Science'
    assert p.years == 2, 'Years should be 2'