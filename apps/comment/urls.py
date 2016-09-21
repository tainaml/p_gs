from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [

    # Translators: URL de pagina de salvar comentario
    url(_(r'^save/$'), views.CommentSaveView.as_view(), name='save'),

    # Translators: URL de pagina de salvar resposta
    url(_(r'^answer-save/$'), views.CommentSaveAnswer.as_view(), name='answer-save'),

    # Translators: URL de pagina de edicao de comentarios
    url(_(r'^edit/$'), views.CommentUpdateView.as_view(), name='edit'),

    # Translators: URL de pagina de edicao de resposta
    url(_(r'^edit-answer/$'), views.CommentUpdateAnswerView.as_view(), name='edit-answer'),

    # Translators: URL de pagina de listagem de respostas
    url(_(r'^list-answer/$'), views.CommentAnswerList.as_view(), name='list-answer'),

    # Translators: URL de pagina atualizacao de comentarios
    url(_(r'^update/$'), views.CommentUpdateView.as_view(), name='update'),

    # Translators: URL de pagina de listagem de comentarios
    url(_(r'^list/$'), views.CommentList.as_view(), name='list'),

    # Translators: URL de pagina de delete de comentario
    url(_(r'^delete$'), views.CommentDeleteView.as_view(), name='delete'),

    # Translators: URL de pagina de contagem de comentario
    url(_(r'^count/(?P<object_to_link>\d+)/(?P<content_type>[a-z]+)$'), views.CommentCountView.as_view(), name='count')
]