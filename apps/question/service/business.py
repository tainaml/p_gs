from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..models import Question, Answer


def save_question(logged_user, params=None):

    question = Question()

    question.title = params["title"]
    question.slug = params["slug"]
    question.author = logged_user
    question.description = params["description"]

    question.save()
    return question


def update_question(params=None, question=None):

    return False if question.save() is False else question


def comment_reply(params=None, logged_user=None, question_id=None):

    answer = Answer()

    answer.description = params["description"]
    answer.author = logged_user
    question = get_question(question_id)
    answer.question = question

    answer.save()
    return answer

def get_answers_by_question(question=None, items_per_page=None, page=None):
    answers = get_all_answers_by_question(question)

    items_per_page = items_per_page if items_per_page else 10

    answers_paginated = Paginator(answers, items_per_page)

    try:
        answers_paginated = answers_paginated.page(page)
    except PageNotAnInteger:
        answers_paginated = answers_paginated.page(1)
    except EmptyPage:
        answers_paginated = []

    return answers_paginated

def get_all_answers_by_question(question=None):
    return Answer.objects.filter(
        question_id=question.id
    ).order_by("-answer_date")




def update_reply(params=None, answer=None):
    answer.description = params['description']
    return False if answer.save() is False else answer


def get_question(question_id=None):
    try:
        quest = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        quest = False

    return quest


def get_answer(answer_id=None):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        answer = False

    return answer


def set_correct_answer(answer_id):

    answer = get_answer(answer_id)

    if answer:
        question = get_question(answer.question.id)
        if question:

            if question.correct_answer and question.correct_answer == answer:
                question.correct_answer = None
            else:
                question.correct_answer = answer

            question.save()
            return question

        else:
            raise Question.DoesNotExist
    else:
        raise Answer.DoesNotExist

def get_own_answer(user=None, **kwargs):
    try:
        return Answer.objects.get(author=user, **kwargs)
    except Answer.DoesNotExist:
        return False




def get_questions_by_user(author):
    try:
        quests = Question.objects.get(author=author)
    except Question.DoesNotExist:
        quests = False

    return quests