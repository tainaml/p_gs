from django.contrib.contenttypes.models import ContentType
from apps.comment.service.forms import CreateCommentForm, EditCommentForm

__author__ = 'phillip'
from django import template
register = template.Library()


@register.inclusion_tag('comment/box-comment.html', takes_context=True)
def comment_box(context, content_object, **kwargs):
    request = context['request']
    form = CreateCommentForm(user=request.user)
    content_type = ContentType.objects.get_for_model(content_object)

    return {
        'form': form,
        'content_object': content_object,
        'content_type': content_type,
        'request': request
    }

@register.inclusion_tag('comment/create-comment.html', takes_context=True)
def comment_box_inner(context, content_object, to_update, **kwargs):
    request = context['request']
    form = CreateCommentForm(user=request.user)
    content_type = ContentType.objects.get_for_model(content_object)

    return {
        'form': form    ,
        'content_object': content_object,
        'content_type': content_type,
        'to_update': to_update,
        'request': request
    }

@register.inclusion_tag('comment/list-container.html', takes_context=True)
def comment_list(context, content_object, **kwargs):

    content_type = ContentType.objects.get_for_model(content_object)
    return {
        'content_object': content_object,
        'content_type': content_type
    }

@register.inclusion_tag('comment/edit-comment.html', takes_context=True)
def comment_edit(context, content_object, **kwargs):

    content_type = ContentType.objects.get_for_model(content_object)
    request = context['request']
    form = EditCommentForm(user=request.user, instance=content_object, data={'content': content_object.content})
    return {
        'content_object': content_object,
        'content_type': content_type,
        'form': form,
        'request': request
    }

@register.inclusion_tag('comment/create-comment.html', takes_context=True)
def comment_create(context, content_object, to_update, **kwargs):

    content_type = ContentType.objects.get_for_model(content_object)

    form = CreateCommentForm()
    return {
        'content_object': content_object,
        'content_type': content_type,
        'form': form,
        'to_update': to_update,
        'request': context['request']
    }
