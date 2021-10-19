from src.regex import matching_first_potential_matrice


def test_matching_first_potential_matrice():
    assert matching_first_potential_matrice(string="[[]]+123213f8j9984j3r") == "[[]]"
    assert matching_first_potential_matrice(string="[[]54654546") == None
    assert matching_first_potential_matrice(string="[[]54654546]+[[]]") == "[[]54654546]"
    assert (
        matching_first_potential_matrice(string="[[14,-+15];[(5+2i)*3,12/4]] + [[5,2];[4,6]]")
        == "[[14,-+15];[(5+2i)*3,12/4]]"
    )
