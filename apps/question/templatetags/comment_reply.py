from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from apps.question.models import Answer
from django import template
register = template.Library()



@register.inclusion_tag('question/comments.html')
def list_reply(question_id):

    try:

        list_comment = Answer.objects.filter(question=question_id).order_by('-answer_date')

    except ValueError:
        raise Http404()

    return {
        'list_comment': list_comment
    }