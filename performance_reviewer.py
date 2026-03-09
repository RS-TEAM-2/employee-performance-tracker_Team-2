from datetime import date
from db_connections import get_mongo_collection


def submit_performance_review(employee_id, reviewer_name, overall_rating,
                               strengths, areas_for_improvement,
                               comments, goals_for_next_period):
    collection = get_mongo_collection()
    review = {
        "employee_id": employee_id,
        "review_date": str(date.today()),
        "reviewer_name": reviewer_name,
        "overall_rating": float(overall_rating),
        "strengths": strengths,
        "areas_for_improvement": areas_for_improvement,
        "comments": comments,
        "goals_for_next_period": goals_for_next_period
    }
    result = collection.insert_one(review)
    print(f"Review submitted successfully. ID: {result.inserted_id}")
    return True


def get_performance_reviews_for_employee(employee_id):
    collection = get_mongo_collection()
    reviews = list(collection.find({"employee_id": employee_id}))
    for r in reviews:
        r["_id"] = str(r["_id"])
    return reviews