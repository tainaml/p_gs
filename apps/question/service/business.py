from ..models import Question


def save_question(question, data):
    return question.save()
