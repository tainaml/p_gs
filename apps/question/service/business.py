from ..models import Question, Answer


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


def comment_reply(params=None, logged_user=None, question_id=None):

    answer = Answer()

    answer.description = params["description"]
    answer.author = logged_user
    question = get_question(question_id)
    answer.question = question

    answer.save()
    return answer


def update_reply(params=None, answer=None):

    answer.description = params["description"]

    answer.save()
    return answer


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