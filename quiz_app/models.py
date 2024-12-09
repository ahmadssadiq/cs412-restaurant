"""
File: models.py
Author: Ahmad Sadiq U37206345
Date: 12/04/24

description: this files define the database models for the Quiz application. These models represent
    the core entities and their relationships, including quizzes, questions, answers, 
    and user attempts. The models leverage Django's ORM to interact with the database,
    ensuring efficient data management and querying.

1. Quiz:
        - Represents a quiz created by a user.
        - Fields:
            - title: The title of the quiz.
            - description: A brief description of the quiz.
            - category: The category to which the quiz belongs (e.g., Science, Math).
            - difficulty: The difficulty level of the quiz (e.g., Easy, Medium, Hard).
            - owner: The user who created the quiz (ForeignKey to Django's User model).
            - created_at: The timestamp for when the quiz was created.
        - Relationships:
            - One-to-Many with the Question model.
2. Question:
        - Represents individual questions within a quiz.
        - Fields:
            - quiz: The quiz to which this question belongs (ForeignKey to Quiz).
            - text: The question text/content.
            - question_type: The type of question (e.g., Multiple Choice, True/False).
            - points: The number of points awarded for correctly answering the question.
        - Relationships:
            - One-to-Many with the Answer model.
3. Answer:
        - Represents possible answers to a specific question.
        - Fields:
            - question: The question to which this answer belongs (ForeignKey to Question).
            - text: The content of the answer.
            - is_correct: Boolean indicating whether this answer is correct.
        - Relationships:
            - Belongs to a single Question.
4. QuizAttempt:
        - Tracks individual user attempts at taking a quiz.
        - Fields:
            - user: The user who attempted the quiz (ForeignKey to Django's User model).
            - quiz: The quiz that was attempted (ForeignKey to Quiz).
            - score: The score achieved by the user for the attempt.
            - time_taken: The time (in seconds) the user took to complete the quiz.
            - completed_at: The timestamp for when the quiz attempt was completed.
        - Relationships:
            - Belongs to a single User and a single Quiz.
5. UserAnswer:
        - Tracks a user's answer to a specific question in a quiz attempt.
        - Fields:
            - quiz_attempt: The quiz attempt to which this answer belongs (ForeignKey to QuizAttempt).
            - question: The question being answered (ForeignKey to Question).
            - selected_answer: The answer selected by the user (ForeignKey to Answer, nullable).
            - is_correct: Boolean indicating whether the selected answer is correct.
        - Relationships:
            - Belongs to a single QuizAttempt and a single Question.
"""

from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=50)
    points = models.IntegerField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    time_taken = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s attempt at {self.quiz.title}"


class UserAnswer(models.Model):
    """
    Tracks a user's answer to a specific question in a quiz.
    """

    quiz_attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, related_name="user_answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(
        Answer, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Automatically calculate whether the selected answer is correct when saving.
        """
        if self.selected_answer:
            self.is_correct = self.selected_answer.is_correct
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quiz_attempt.user.username}'s answer to '{self.question.text}'"
