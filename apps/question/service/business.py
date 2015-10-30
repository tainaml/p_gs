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


def update_reply(params=None, answer=None):

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


def get_questions_by_user(author):
    try:
        quests = Question.objects.get(author=author)
    except Question.DoesNotExist:
        quests = False

    return quests