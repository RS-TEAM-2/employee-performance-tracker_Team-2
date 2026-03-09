import pytest
from performance_reviewer import submit_performance_review, get_performance_reviews_for_employee


def test_submit_review_success(mongo_col):
    result = submit_performance_review(
        1,
        "Anita Desai",
        4.5,
        ["Problem solving", "Team work"],
        ["Documentation"],
        "Great performance this quarter.",
        ["Lead a project"]
    )
    assert result == True


def test_get_reviews_for_employee(mongo_col):
    submit_performance_review(
        1,
        "Anita Desai",
        4.5,
        ["Problem solving", "Team work"],
        ["Documentation"],
        "Great performance this quarter.",
        ["Lead a project"]
    )
    reviews = get_performance_reviews_for_employee(1)
    assert len(reviews) == 1
    assert reviews[0]["overall_rating"] == 4.5
    assert reviews[0]["reviewer_name"] == "Anita Desai"


def test_get_reviews_empty(mongo_col):
    reviews = get_performance_reviews_for_employee(999)
    assert reviews == []


def test_multiple_reviews_for_same_employee(mongo_col):
    submit_performance_review(1, "Reviewer A", 4.0, ["Skill A"], ["Area A"], "Good.", ["Goal A"])
    submit_performance_review(1, "Reviewer B", 3.5, ["Skill B"], ["Area B"], "Okay.", ["Goal B"])
    reviews = get_performance_reviews_for_employee(1)
    assert len(reviews) == 2


def test_reviews_isolated_per_employee(mongo_col):
    submit_performance_review(
        1,
        "Anita Desai",
        4.5,
        ["Problem solving"],
        ["Documentation"],
        "Great performance.",
        ["Lead a project"]
    )
    reviews_emp1 = get_performance_reviews_for_employee(1)
    reviews_emp2 = get_performance_reviews_for_employee(2)
    assert len(reviews_emp1) == 1
    assert len(reviews_emp2) == 0


def test_review_rating_stored_as_float(mongo_col):
    submit_performance_review(
        1,
        "Anita Desai",
        4,
        ["Problem solving"],
        ["Documentation"],
        "Good.",
        ["Goal"]
    )
    reviews = get_performance_reviews_for_employee(1)
    assert isinstance(reviews[0]["overall_rating"], float)