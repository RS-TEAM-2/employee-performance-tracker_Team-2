import pytest
from performance_reviewer import submit_performance_review, get_performance_reviews_for_employee

def test_submit_and_get_review(mock_nosql_db):
    """Tests submission and retrieval of NoSQL review documents[cite: 145]."""
    review_data = {
        "employee_id": 1,
        "review_date": "2024-12-01",
        "reviewer_name": "Manager X",
        "overall_rating": 5,
        "strengths": "Problem solving",
        "areas_for_improvement": "Public speaking",
        "comments": "Great year!",
        "goals_for_next_period": "Lead a team"
    }
    
    # Submit to mock MongoDB [cite: 100]
    submit_performance_review(**review_data)
    
    # Retrieve [cite: 101]
    reviews = get_performance_reviews_for_employee(1)
    assert len(reviews) == 1
    assert reviews[0]['overall_rating'] == 5