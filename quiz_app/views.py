"""
File: views.py
Author: Ahmad Sadiq U37206345
Date: 12/04/24

Description: This file defines the views for the Quiz application. Views handle the interaction 
between the user and the server by processing HTTP requests and returning appropriate responses. 
Each view corresponds to a specific functionality, such as user authentication, quiz creation, 
playing a quiz, and displaying results.

Views in this file:
1. index: Displays the list of available quizzes on the home page, with optional filtering by difficulty.
2. sign_up: Handles user registration.
3. sign_in: Handles user login.
4. sign_out: Logs out the user and redirects to the login page.
5. create_quiz: Allows authenticated users to create a quiz with questions and answers.
6. play_quiz: Fetches and displays a specific quiz for the user to attempt.
7. check_answer: Verifies if a selected answer is correct and returns the result as JSON.
8. submit_quiz: Processes user-submitted answers, calculates the score, and saves the attempt.
9. quiz_results: Displays the results of a quiz attempt.
10. edit_quiz: Allows authenticated users to edit an existing quiz.
11. delete_quiz: Allows authenticated users to delete an existing quiz.
"""

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Question, Answer, Quiz, QuizAttempt
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, QuizForm, QuestionFormSet, AnswerFormSet
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    """
    Displays the list of available quizzes on the home page, with optional filtering by difficulty.
    Parameters:
        request: The HTTP request object.
    Returns:
        HttpResponse: Renders the 'index.html' template with filtered quizzes and the user object.
    """
    # Get the difficulty filter from query parameters
    difficulty = request.GET.get("difficulty")

    # Filter quizzes based on difficulty, or show all quizzes if no filter is applied
    if difficulty:
        quizzes = Quiz.objects.filter(difficulty=difficulty)
    else:
        quizzes = Quiz.objects.all()

    context = {
        "quizzes": quizzes,
        "user": request.user,  # Pass the user object to the template
        "selected_difficulty": difficulty,  # Pass the selected difficulty to the template
    }
    return render(request, "quiz_app/index.html", context)


def sign_up(request):
    """
    Handles user registration.
    Parameters:
        request: The HTTP request object.
    Returns:
        HttpResponse: Renders the 'sign_up.html' template with the registration form,
        or redirects to 'index' upon successful registration.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after sign-up
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "quiz_app/sign_up.html", {"form": form})


def sign_in(request):
    """
    Handles user login.
    Parameters:
        request: The HTTP request object.
    Returns:
        HttpResponse: Renders the 'sign_in.html' template with the login form,
        or redirects to 'index' upon successful login.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")  # Redirect to the index page
    else:
        form = AuthenticationForm()
    return render(request, "quiz_app/sign_in.html", {"form": form})


@login_required
def sign_out(request):
    """
    Logs out the user and redirects to the login page.
    Parameters:
        request: The HTTP request object.
    Returns:
        HttpResponseRedirect: Redirects to the 'sign_in' page.
    """
    logout(request)
    return redirect("sign_in")


@login_required
def create_quiz(request):
    """
    Allows authenticated users to create a quiz with questions and answers.
    Parameters:
        request: The HTTP request object.
    Returns:
        HttpResponse: Renders the 'create_quiz.html' template with a quiz form,
        or redirects to 'index' upon successful quiz creation.
    """
    if request.method == "POST":
        print(request.POST)  # Debugging: Print all POST data

        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            # Save the quiz
            quiz = quiz_form.save(commit=False)
            quiz.owner = request.user
            quiz.save()

            # Loop through the questions provided in the form
            question_index = 0
            while f"questions[{question_index}][text]" in request.POST:
                question_text = request.POST.get(f"questions[{question_index}][text]")
                print(f"Question: {question_text}")  # Debugging

                # Create a new question
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    question_type=request.POST.get(
                        f"questions[{question_index}][question_type]", "text"
                    ),
                    points=int(
                        request.POST.get(f"questions[{question_index}][points]", 0)
                    ),
                )

                # Loop through answers for the question
                answer_index = 0
                while (
                    f"questions[{question_index}][answers][{answer_index}][text]"
                    in request.POST
                ):
                    answer_text = request.POST.get(
                        f"questions[{question_index}][answers][{answer_index}][text]"
                    )
                    is_correct = (
                        request.POST.get(
                            f"questions[{question_index}][answers][{answer_index}][is_correct]",
                            "off",
                        )
                        == "on"
                    )
                    print(
                        f"Answer {answer_index}: {answer_text}, Is Correct: {is_correct}"
                    )  # Debugging

                    # Create the answer
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=is_correct,
                    )
                    answer_index += 1

                question_index += 1

            return redirect("index")  # Redirect to the homepage
    else:
        # Load an empty quiz form for GET requests
        quiz_form = QuizForm()
    return render(request, "quiz_app/create_quiz.html", {"quiz_form": quiz_form})


@login_required
def play_quiz(request, quiz_id):
    """
    Fetches and displays a specific quiz for the user to attempt.
    Parameters:
        request: The HTTP request object.
        quiz_id: The ID of the quiz to be played.
    Returns:
        HttpResponse: Renders the 'play_quiz.html' template with the quiz and its questions.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Fetch the quiz
    questions = quiz.questions.all()  # Get all questions for the quiz

    context = {
        "quiz": quiz,
        "questions": questions,  # Pass all questions to the template
    }
    return render(request, "quiz_app/play_quiz.html", context)


def check_answer(request, question_id):
    """
    Verifies if the selected answer for a question is correct.
    Parameters:
        request: The HTTP request object.
        question_id: The ID of the question being answered.
    Returns:
        JsonResponse: A JSON response indicating whether the answer is correct.
    """
    question = Question.objects.get(id=question_id)
    selected_answer_id = request.POST.get("answer")
    selected_answer = Answer.objects.get(id=selected_answer_id)
    is_correct = selected_answer.is_correct
    return JsonResponse({"correccreatet": is_correct})


@login_required
def submit_quiz(request, quiz_id):
    """
    Processes user-submitted answers, calculates the score, and saves the quiz attempt.
    Parameters:
        request: The HTTP request object.
        quiz_id: The ID of the quiz being submitted.
    Returns:
        HttpResponseRedirect: Redirects to the quiz results page.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Get all questions for the quiz
    total_questions = questions.count()
    correct_answers = 0

    # Calculate the score based on user responses
    for question in questions:
        user_answer_id = request.POST.get(
            f"question_{question.id}"
        )  # Fetch user's answer for this question
        if user_answer_id:
            user_answer = Answer.objects.filter(id=user_answer_id).first()
            if user_answer and user_answer.is_correct:
                correct_answers += 1

    # Save the attempt
    QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=correct_answers,
        time_taken=0,  # Placeholder for future time tracking
    )

    # Redirect to results page
    return redirect(
        "quiz_results", quiz_id=quiz.id, score=correct_answers, total=total_questions
    )


@login_required
def quiz_results(request, quiz_id, score, total):
    """
    Displays the results of a quiz attempt.
    Parameters:
        request: The HTTP request object.
        quiz_id: The ID of the quiz.
        score: The score achieved by the user.
        total: The total number of questions in the quiz.
    Returns:
        HttpResponse: Renders the 'quiz_results.html' template with the quiz and score details.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        "quiz": quiz,
        "score": score,
        "total": total,
    }
    return render(request, "quiz_app/quiz_results.html", context)


@login_required
def edit_quiz(request, quiz_id):
    """
    Allows authenticated users to edit an existing quiz.
    Parameters:
        request: The HTTP request object.
        quiz_id: The ID of the quiz to be edited.
    Returns:
        HttpResponse: Renders the 'edit_quiz.html' template with the quiz form pre-filled
        with the current quiz data, or redirects to 'index' upon successful edit.
    """
    # Fetch the quiz object owned by the current user or return 404 if not found
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)

    if request.method == "POST":
        # Bind the form with POST data and the existing quiz instance
        quiz_form = QuizForm(request.POST, instance=quiz)
        if quiz_form.is_valid():
            # Save the updated quiz details
            quiz_form.save()
            return redirect("index")  # Redirect to the homepage after editing
    else:
        # Load the form with the current quiz instance for GET requests
        quiz_form = QuizForm(instance=quiz)

    # Render the edit page with the quiz form
    context = {"quiz_form": quiz_form, "quiz": quiz}
    return render(request, "quiz_app/edit_quiz.html", context)


@login_required
def delete_quiz(request, quiz_id):
    """
    Allows authenticated users to delete an existing quiz.
    Parameters:
        request: The HTTP request object.
        quiz_id: The ID of the quiz to be deleted.
    Returns:
        HttpResponseRedirect: Redirects to the 'index' page upon successful deletion.
        HttpResponse: Renders the 'delete_quiz.html' template to confirm the deletion.
    """
    # Fetch the quiz object owned by the current user or return 404 if not found
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)

    if request.method == "POST":
        # Delete the quiz if the user confirms the action
        quiz.delete()
        return redirect("index")  # Redirect to the homepage after deletion

    # Render the confirmation page for quiz deletion
    context = {"quiz": quiz}
    return render(request, "quiz_app/delete_quiz.html", context)
