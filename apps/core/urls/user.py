from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.userprofile import views
from ..views import user as core_user

urlpatterns = [

    # Translators: URL de edicao de usuario
    url(_(r'^edit/$'), core_user.CoreProfileEdit.as_view(), name='edit'),

    # Translators: URL de edicao via ajax
    url(_(r'^edit/ajax/$'), core_user.CoreProfileEditAjax.as_view(), name='edit-ajax'),

    # Translators: URL de edicao de posts
    url(_(r'^edit-posts/$'), core_user.CoreProfileSearchEditPosts.as_view(), name='edit-posts'),

    # Translators: URL de procura de posts
    url(_(r'^edit-posts/search/$'), core_user.CoreProfileSearchEditPostsAjax.as_view(), name='edit-posts-search-ajax'),

    # Translators: URL de listagem e procura de posts
    url(_(r'^edit-posts/search/list/$'), core_user.CoreProfileSearchEditPostsList.as_view(), name='edit-posts-list'),

    # Translators: URL de passo 1 do wizard
    url(_(r'^wizard/step/personal-info$'), core_user.CoreProfileWizardStepOneAjax.as_view(), name='wizard-step-personal-info-ajax'),

    # Translators: URL de passo 2 do wizard
    url(_(r'^wizard/step/filter-categories$'), core_user.CoreProfileWizardStepTwoAjax.as_view(), name='wizard-step-filter-categories-ajax'),

    # Translators: URL de passo 3 do wizard
    url(_(r'^wizard/step/filter-categories/list$'), core_user.CoreProfileWizardStepTwoListAjax.as_view(), name='wizard-step-filter-categories-list-ajax'),

    # Translators: URL de sugestoes do usuario
    url(_(r'^wizard/step/suggestions$'), core_user.CoreProfileWizardStepThreeAjax.as_view(), name='wizard-step-suggestion-ajax'),

    # Translators: URL para retornar o estado
    url(_(r'^get_state/$'), views.ProfileGetState.as_view(), name='get_state'),

    # Translators: URL para retornar a cidade
    url(_(r'^get_city/$'), views.ProfileGetCity.as_view(), name='get_city'),

    # Translators: URL para exibir as ocupacoes do usuario
    url(_(r'^occupation/$'), views.OccupationManageView.as_view(), name='occupation_manage'),

    # Translators: URL para adicionar ocupacoes
    url(_(r'^occupation/add/$'), views.OccupationAddView.as_view(), name='occupation_add'),

    # Translators: URL para retornar uma ocupacao
    url(_(r'^occupation/(?P<occupation_id>[0-9]+)/$'), views.OccupationShowView.as_view(), name='occupation_show'),

    # Translators: URL para edicao de ocupacao
    url(_(r'^occupation/edit/(?P<occupation_id>[0-9]+)/$'), views.OccupationEditView.as_view(), name='occupation_edit'),

    # Translators: URL para deletar ocupacao
    url(_(r'^occupation/delete/(?P<occupation_id>[0-9]+)/$'), views.OccupationDeleteView.as_view(), name='occupation_delete'),

    # Translators: URL de feed
    url(_(r'^feed/$'), core_user.CoreUserFeed.as_view(), name='feed'),

    # Translators: URL de listagem de feed
    url(_(r'^list$'), core_user.CoreUserList.as_view(), name='feed-list'),

    # Translators: URL de listagem e publicacoes do usuario
    url(_(r'^list_articles/(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$'), core_user.CoreUserList.as_view(), name='list_articles'),

    # Translators: URL de ver depois do usuario
    url(_(r'^ver-depois$'), core_user.SocialActionSeeLater.as_view(), name='see-later'),

    # Translators: URL de listagem de ver depois
    url(_(r'^ver-depois/list$'), core_user.SocialActionSeeLaterList.as_view(), name='see-later-list'),

    # Translators: URL de remover ver depois
    url(_(r'^remover-ver-depois$'), core_user.SocialActionRemoveSeeLater.as_view(), name='remove-see-later'),

    # Translators: URL de favoritos
    url(_(r'^favoritos$'), core_user.SocialActionFavourite.as_view(), name='favourite'),

    # Translators: URL de listagem de favoritos
    url(_(r'^favoritos/list$'), core_user.SocialActionFavouriteList.as_view(), name='favourite-list'),

    # Translators: URL de desfavoritar
    url(_(r'^desfavoritar$'), core_user.SocialActionRemoveFavourite.as_view(), name='unfavourite'),

    # Translators: URL de sugestoes
    url(_(r'^sugestoes$'), core_user.SocialActionSuggest.as_view(), name='suggest'),

    # Translators: URL de listagem de sugestoes
    url(_(r'^sugestoes/list/$'), core_user.SocialActionSuggestList.as_view(), name='suggestList'),

    # Translators: URL de remover sugestao
    url(_(r'^remover-sugestao/$'), core_user.SocialActionRemoveSuggest.as_view(), name='unsuggest'),

    # Translators: URL de listagem de acoes sociais
    url(_(r'^items/list/(?P<action>[a-z]+(?:-[a-z]+)*)/$'), core_user.SocialActionListItems.as_view(), name='list-socialactions-items'),

    # Translators: URL para mostrar usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$'), core_user.CoreUserProfile.as_view(), name='show'),

    # Translators: URL da listagem de perfil do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/list$'), core_user.CoreUserProfileList.as_view(), name='list'),

    # Translators: URL de busca de usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/search$'), core_user.CoreUserSearch.as_view(), name='search'),

    # Translators: URL de seguidores do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/$'), views.ProfileFollowingsView.as_view(), name='followings'),

    # Translators: URL de procura de seguindo de usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/search/$'), core_user.CoreProfileFollowingsSearch.as_view(), name='followings-search'),

    # Translators: URL de listagem de procura de usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/search/list/$'), core_user.CoreProfileFollowingsSearchList.as_view(), name='followings-search-list'),

    # Translators: URL de carregamento assincrono de seguindo
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/load/ajax/$'), core_user.CoreProfileFollowingsLoadAjax.as_view(), name='followings-load-ajax'),

    # Translators: URL root de seguidores
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$'), views.ProfileFollowersView.as_view(), name='followers'),

    # Translators: URL de procura de seguidores
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/search/$'), core_user.CoreProfileFollowersSearch.as_view(), name='followers-search'),

    # Translators: URL de listagem de busca de seguidores
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/search/list/$'), core_user.CoreProfileFollowersSearchList.as_view(), name='followers-search-list'),

    # Translators: URL de comunidades do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/$'), core_user.CoreProfileCommunitiesSearchView.as_view(), name='communities'),

    # Translators: URL de listagem de comunidades do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/list/$'), core_user.CoreProfileCommunitiesSearchListView.as_view(), name='communities-list'),

    # Translators: URL de carregamento assincrono de comunidades do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/load/ajax/$'), core_user.CoreProfileCommunitiesLoadAjax.as_view(), name='communities-load-ajax'),

    # Translators: URL de videos do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/$'), core_user.CoreProfileVideosView.as_view(), name='videos'),

    # Translators: URL de procura de videos do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/$'), core_user.CoreProfileVideosSearch.as_view(), name='videos-search'),

    # Translators: URL de listagem de busca de videos do usuario
    url(_(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/list/$'), core_user.CoreProfileVideosList.as_view(), name='videos-search-list'),

    # Translators: URL de carregamento assincrono de comunidades do usuario
    url(_(r'^ajax/user/communities/$'), core_user.CoreUserCommunitiesListAjax.as_view(), name='user-communities-ajax'),
]