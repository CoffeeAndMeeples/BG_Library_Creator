import bg_library
import pytest

dict_object = {"name": "Catan", "id": "13"}
string_object = "Catan"

def main():
    ...

def test_search():
    assert bg_library.search("Catan") == "13"
    assert bg_library.search("asdf") == None
    assert bg_library.search("catan") == "13"


def test_print_games():

    assert bg_library.print_games(dict_object) == 0
    assert bg_library.print_games(string_object) == 0



def test_create_game():
    with pytest.raises(TypeError):
        bg_library.create_game()





if __name__=="__main__":
    main()
