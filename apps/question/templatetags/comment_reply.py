from apps.question.service.forms import EditAnswerForm
from django.http import Http404
from django import template

from apps.question.models import Answer

register = template.Library()



@register.inclusion_tag('question/comments.html', takes_context=True)
def list_reply(context, question_id):

    try:
        list_comment = Answer.objects.filter(question=question_id).order_by('-answer_date')
    except ValueError:
        raise Http404()

    return {
        'list_comment': list_comment,
        'request': context['request']
    }


@register.inclusion_tag('question/edit_answer.html', takes_context=True)
def answer_edit_box(context, answer):

    user = None

    request = context.get('request')
    if request:
        user = request.user

    form = EditAnswerForm(instance=answer, user=user)

    return {
        'form': form,
        'answer': answer
    }
