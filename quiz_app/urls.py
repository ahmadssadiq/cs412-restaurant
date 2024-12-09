"""
File: urls.py
Author: Ahmad Sadiq U37206345
Date: 12/04/24

Description: This file defines the URL routing for the Quiz application. 
It maps specific URL patterns to their corresponding view functions, enabling 
users to interact with different features of the application. The urlpatterns list
is used by Django to match incoming HTTP requests with appropriate views.

URL Patterns:
1. index: Root view of the application (home page).
2. sign_up: URL for user registration.
3. sign_in: URL for user login.
4. sign_out: URL for user logout.
5. create_quiz: URL for quiz creation.
6. play_quiz: URL to play a specific quiz, identified by quiz_id.
7. check_answer: URL to check the user's answer for a specific question, identified by question_id.
8. submit_quiz: URL to submit answers for a quiz, identified by quiz_id.
9. quiz_results: URL to display quiz results, showing the quiz_id, the user's score, and the total score.
"""

from django.urls import path
from .views import (
    sign_up,
    sign_in,
    sign_out,
    create_quiz,
    play_quiz,
    check_answer,
    index,
    submit_quiz,
    quiz_results,
)

# Define urlpatterns to map URLs to their corresponding view functions
urlpatterns = [
    path("", index, name="index"),  # Root view for the app
    path("sign_up/", sign_up, name="sign_up"),  # User registration page
    path("sign_in/", sign_in, name="sign_in"),  # User login page
    path("sign_out/", sign_out, name="sign_out"),  # User logout action
    path("create_quiz/", create_quiz, name="create_quiz"),  # Page to create a new quiz
    path(
        "play_quiz/<int:quiz_id>/", play_quiz, name="play_quiz"
    ),  # Page to play a specific quiz
    path(
        "check_answer/<int:question_id>/", check_answer, name="check_answer"
    ),  # Endpoint to check answers
    path(
        "submit_quiz/<int:quiz_id>/", submit_quiz, name="submit_quiz"
    ),  # Endpoint to submit quiz answers
    path(
        "quiz_results/<int:quiz_id>/<int:score>/<int:total>/",
        quiz_results,
        name="quiz_results",
    ),  # Display quiz results
]
