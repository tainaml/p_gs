from ..models import Question


def save_question(logged_user, params=None):

    question = Question()

    question.title = params["title"]
    question.author = logged_user
    question.description = params["description"]

    question.save()
    return question


def update_question(params=None, question=None):

    question.title = params["title"]
    question.description = params["description"]

    question.save()
    return question


def get_question(question_id=None):
    try:
        quest = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        quest = False

    return quest