from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.question import views
from ..views import question as CoreViews

urlpatterns = [

    # Translators: URL para criar pergunta
    url(_(r'^create/$'), CoreViews.CoreQuestionCreateView.as_view(), name='create'),

    # Translators: URL para salvar pergunta
    url(_(r'^save/$'), CoreViews.CoreSaveQuestionView.as_view(), name='save'),

    # Translators: URL para editar pergunta
    url(_(r'^edit/(?P<question_id>[0-9]+)$'), CoreViews.CoreEditQuestionView.as_view(), name='edit'),

    # Translators: URL para deletar pergunta
    url(_(r'^delete/(?P<question_id>[0-9]+)$'), CoreViews.CoreDeleteQuestionView.as_view(), name='delete'),
    url(_(r'^delete/async/(?P<question_id>\d+)$'), CoreViews.CoreDeleteQuestionView.as_view(), name='delete-async'),

    # Translators: URL para atualizar pergunta
    url(_(r'^update/$'), CoreViews.CoreUpdateQuestionView.as_view(), name='update'),

    # Translators: URL para comentar resposta
    url(_(r'^comment-reply/$'), views.CommentReplayView.as_view(), name='comment_reply'),

    # Translators: URL para listagem de resposta
    url(_(r'^answer-list/$'), views.AnswerList.as_view(), name='answer_list'),

    # Translators: URL de atualizar respota
    url(_(r'^update_reply/$'), views.UpdateReplyView.as_view(), name='update_reply'),

    # Translators: URL de carregar perguntas relacionadas
    url(_(r'^load/related/(?P<question_id>[0-9]+)/(?P<content_type>[a-z]+)/$'), CoreViews.CoreQuestionRelatedView.as_view(), name='related-questions-async'),

    # Translators: URL para marcar resposta correta
    url(_(r'^correct-answer/(?P<answer_id>[0-9]+)$'), views.CorrectAnswer.as_view(), name='correct-answer'),

    # Translators: URL remover resposta
    url(_(r'^remove-answer$'), views.RemoveAnswer.as_view(), name='remove-answer'),

    # Translators: URL visualizacao de pergunta
    url(_(r'^(?P<question_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/(?P<question_id>[0-9]+)/$'), CoreViews.CoreQuestionView.as_view(), name='show'),

    # Create question in community
    # Translators: URL de criar pergunta
    url(_(r'^create/(?P<community_slug>[a-z0-9]+(?:-[a-z0-9]+)*)$'), CoreViews.CoreQuestionInCommunityView.as_view(), name='create-in-category'),

]
