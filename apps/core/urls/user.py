from django.conf.urls import url

from apps.userprofile import views
from ..views import user as core_user

urlpatterns = [

    url(r'^edit/$', core_user.CoreProfileEdit.as_view(), name='edit'),
    url(r'^edit/ajax/$', core_user.CoreProfileEditAjax.as_view(), name='edit-ajax'),

    url(r'^edit-posts/$', core_user.CoreProfileSearchEditPosts.as_view(), name='edit-posts'),
    url(r'^edit-posts/search/$', core_user.CoreProfileSearchEditPostsAjax.as_view(), name='edit-posts-search-ajax'),
    url(r'^edit-posts/search/list/$', core_user.CoreProfileSearchEditPostsList.as_view(), name='edit-posts-list'),

    url(r'^wizard/step/personal-info$', core_user.CoreProfileWizardStepOneAjax.as_view(), name='wizard-step-personal-info-ajax'),
    url(r'^wizard/step/filter-categories$', core_user.CoreProfileWizardStepTwoAjax.as_view(), name='wizard-step-filter-categories-ajax'),
    url(r'^wizard/step/filter-categories/list$', core_user.CoreProfileWizardStepTwoListAjax.as_view(), name='wizard-step-filter-categories-list-ajax'),
    url(r'^wizard/step/suggestions$', core_user.CoreProfileWizardStepThreeAjax.as_view(), name='wizard-step-suggestion-ajax'),

    url(r'^get_state/$', views.ProfileGetState.as_view(), name='get_state'),
    url(r'^get_city/$', views.ProfileGetCity.as_view(), name='get_city'),

    url(r'^occupation/$', views.OccupationManageView.as_view(), name='occupation_manage'),
    url(r'^occupation/add/$', views.OccupationAddView.as_view(), name='occupation_add'),
    url(r'^occupation/(?P<occupation_id>[0-9]+)/$', views.OccupationShowView.as_view(), name='occupation_show'),
    url(r'^occupation/edit/(?P<occupation_id>[0-9]+)/$', views.OccupationEditView.as_view(), name='occupation_edit'),
    url(r'^occupation/delete/(?P<occupation_id>[0-9]+)/$', views.OccupationDeleteView.as_view(), name='occupation_delete'),

    url(r'^feed/$', core_user.CoreUserFeed.as_view(), name='feed'),
    url(r'^list$', core_user.CoreUserList.as_view(), name='feed-list'),
    url(r'^list_articles/(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', core_user.CoreUserList.as_view(), name='list_articles'),

    url(r'^ver-depois$', core_user.SocialActionSeeLater.as_view(), name='see-later'),
    url(r'^ver-depois/list$', core_user.SocialActionSeeLaterList.as_view(), name='see-later-list'),
    url(r'^remover-ver-depois$', core_user.SocialActionRemoveSeeLater.as_view(), name='remove-see-later'),
    url(r'^favoritos$', core_user.SocialActionFavourite.as_view(), name='favourite'),
    url(r'^favoritos/list$', core_user.SocialActionFavouriteList.as_view(), name='favourite-list'),
    url(r'^desfavoritar$', core_user.SocialActionRemoveFavourite.as_view(), name='unfavourite'),
    url(r'^sugestoes$', core_user.SocialActionSuggest.as_view(), name='suggest'),
    url(r'^sugestoes/list/$', core_user.SocialActionSuggestList.as_view(), name='suggestList'),
    url(r'^remover-sugestao/$', core_user.SocialActionRemoveSuggest.as_view(), name='unsuggest'),
    url(r'^items/list/(?P<action>[a-z]+(?:-[a-z]+)*)/$', core_user.SocialActionListItems.as_view(), name='list-socialactions-items'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', core_user.CoreUserProfile.as_view(), name='show'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/list$', core_user.CoreUserProfileList.as_view(), name='list'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/search$', core_user.CoreUserSearch.as_view(), name='search'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/$', views.ProfileFollowingsView.as_view(), name='followings'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/search/$', core_user.CoreProfileFollowingsSearch.as_view(), name='followings-search'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/search/list/$', core_user.CoreProfileFollowingsSearchList.as_view(), name='followings-search-list'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/load/ajax/$', core_user.CoreProfileFollowingsLoadAjax.as_view(), name='followings-load-ajax'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', views.ProfileFollowersView.as_view(), name='followers'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/search/$', core_user.CoreProfileFollowersSearch.as_view(), name='followers-search'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/search/list/$', core_user.CoreProfileFollowersSearchList.as_view(), name='followers-search-list'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/$', core_user.CoreProfileCommunitiesSearchView.as_view(), name='communities'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/list/$', core_user.CoreProfileCommunitiesSearchListView.as_view(), name='communities-list'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/load/ajax/$', core_user.CoreProfileCommunitiesLoadAjax.as_view(), name='communities-load-ajax'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/$', core_user.CoreProfileVideosView.as_view(), name='videos'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/$', core_user.CoreProfileVideosSearch.as_view(), name='videos-search'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/list/$', core_user.CoreProfileVideosList.as_view(), name='videos-search-list'),

    url(r'^ajax/user/communities/$', core_user.CoreUserCommunitiesListAjax.as_view(), name='user-communities-ajax'),
]