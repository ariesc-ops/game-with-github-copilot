def test_signup_success_adds_participant(client):
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_duplicate_is_rejected_case_insensitive(client):
    existing_with_case_and_spaces = "  Michael@Mergington.edu  "

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_with_case_and_spaces},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_activity_not_found(client):
    response = client.post(
        "/activities/Robotics Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
