"""
File: forms.py
Author: Ahmad Sadiq U37206345
Date: 12/4/24

Description: This file defines the forms used in the Quiz application for user authentication,
quiz creation, and managing questions and answers. The forms leverage Django's built-in
form classes and model forms to simplify data validation and rendering in templates.

Forms in this file:
1. CustomUserCreationForm: Extends Django's UserCreationForm to include an email field for user registration.
2. CustomAuthenticationForm: Custom login form for user authentication.
3. QuizForm: Model form for creating and updating quizzes.
4. QuestionForm: Model form for creating and updating questions in a quiz.
5. AnswerForm: Model form for creating and updating answers to questions.
6. QuestionFormSet: Inline formset for managing multiple questions related to a single quiz.
7. AnswerFormSet: Inline formset for managing multiple answers related to a single question.

Source of how i used inlineformset_factory:
https://techincent.com/explained-django-inline-formset-factory-with-example/
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Quiz, Question, Answer
from django.forms import inlineformset_factory


# Custom user creation form for signing up users
class CustomUserCreationForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to add an email field for user registration.

    Fields:
        - username: The username for the new user.
        - email: The email address for the user (required).
        - password1: The user's password.
        - password2: Confirmation of the user's password.
    """

    email = forms.EmailField(
        required=True, help_text="Required. Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# Custom authentication form for user login
class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form for user authentication.

    Fields:
        - username: The username of the user.
        - password: The user's password.
    """

    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


# Form for Quiz model
class QuizForm(forms.ModelForm):
    """
    Model form for creating and updating quizzes.

    Fields:
        - title: The title of the quiz.
        - description: A brief description of the quiz.
        - category: The category to which the quiz belongs (e.g., Science, Math).
        - difficulty: The difficulty level of the quiz (e.g., Easy, Medium, Hard).
    """

    class Meta:
        model = Quiz
        fields = ["title", "description", "category", "difficulty"]


# Form for Question model
class QuestionForm(forms.ModelForm):
    """
    Model form for creating and updating questions in a quiz.

    Fields:
        - text: The question text/content.
        - question_type: The type of question (e.g., Multiple Choice, True/False).
        - points: The number of points awarded for correctly answering the question.
    """

    class Meta:
        model = Question
        fields = ["text", "question_type", "points"]


# Form for Answer model
class AnswerForm(forms.ModelForm):
    """
    Model form for creating and updating answers to questions.

    Fields:
        - text: The content of the answer.
        - is_correct: Boolean indicating whether this answer is correct.
    """

    class Meta:
        model = Answer
        fields = ["text", "is_correct"]


# Formset for Questions in a Quiz
QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    fields=("text", "question_type", "points"),
    extra=1,  # Start with one empty question form
    can_delete=True,
)

"""
Formset for managing multiple questions related to a single quiz.

Parameters:
    - Quiz: The parent model to which questions belong.
    - Question: The model representing individual questions.
    - form: The form class used for individual questions.
    - fields: Fields to be included in the formset.
    - extra: Number of empty forms to display initially.
    - can_delete: Whether the user can delete questions.
"""

# Formset for Answers in a Question
AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    fields=("text", "is_correct"),
    extra=2,  # Start with two empty answer forms
    can_delete=True,
)

"""
Formset for managing multiple answers related to a single question.

Parameters:
    - Question: The parent model to which answers belong.
    - Answer: The model representing individual answers.
    - form: The form class used for individual answers.
    - fields: Fields to be included in the formset.
    - extra: Number of empty forms to display initially.
    - can_delete: Whether the user can delete answers.
"""
