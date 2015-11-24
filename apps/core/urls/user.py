from django.conf.urls import url
from apps.userprofile import views
from ..views import user as CoreUserProfileView

urlpatterns = [

    url(r'^edit/$', CoreUserProfileView.CoreProfileEdit.as_view(), name='edit'),
    url(r'^edit/ajax/$', CoreUserProfileView.CoreProfileEditAjax.as_view(), name='edit-ajax'),

    url(r'^edit-posts/$', CoreUserProfileView.CoreProfileSearchEditPosts.as_view(), name='edit-posts'),
    url(r'^edit-posts/search/$', CoreUserProfileView.CoreProfileSearchEditPostsAjax.as_view(), name='edit-posts-search-ajax'),
    url(r'^edit-posts/search/list/$', CoreUserProfileView.CoreProfileSearchEditPostsList.as_view(), name='edit-posts-list'),

    url(r'^wizard/step/personal-info$', CoreUserProfileView.CoreProfileWizardStepOneAjax.as_view(), name='wizard-step-personal-info-ajax'),
    url(r'^wizard/step/filter-categories$', CoreUserProfileView.CoreProfileWizardStepTwoAjax.as_view(), name='wizard-step-filter-categories-ajax'),
    url(r'^wizard/step/filter-categories/list$', CoreUserProfileView.CoreProfileWizardStepTwoListAjax.as_view(), name='wizard-step-filter-categories-list-ajax'),
    url(r'^wizard/step/suggestions$', CoreUserProfileView.CoreProfileWizardStepThreeAjax.as_view(), name='wizard-step-suggestion-ajax'),

    url(r'^get_state/$', views.ProfileGetState.as_view(), name='get_state'),
    url(r'^get_city/$', views.ProfileGetCity.as_view(), name='get_city'),

    url(r'^occupation/$', views.OccupationManageView.as_view(), name='occupation_manage'),
    url(r'^occupation/add/$', views.OccupationAddView.as_view(), name='occupation_add'),
    url(r'^occupation/(?P<occupation_id>[0-9]+)/$', views.OccupationShowView.as_view(), name='occupation_show'),
    url(r'^occupation/edit/(?P<occupation_id>[0-9]+)/$', views.OccupationEditView.as_view(), name='occupation_edit'),
    url(r'^occupation/delete/(?P<occupation_id>[0-9]+)/$', views.OccupationDeleteView.as_view(), name='occupation_delete'),

    url(r'^feed/$', CoreUserProfileView.CoreUserFeed.as_view(), name='feed'),
    url(r'^search/(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreUserProfileView.CoreUserSearch.as_view(), name='search'),
    url(r'^list/(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreUserProfileView.CoreUserList.as_view(), name='list'),
    url(r'^list_articles/(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreUserProfileView.CoreUserList.as_view(), name='list_articles'),

    url(r'^ver-depois/$', CoreUserProfileView.SocialActionSeeLater.as_view(), name='see_later'),
    url(r'^remover-ver-depois/$', CoreUserProfileView.SocialActionRemoveSeeLater.as_view(), name='remove_see_later'),
    url(r'^favoritos/$', CoreUserProfileView.SocialActionFavourite.as_view(), name='favourite'),
    url(r'^favoritos/list/$', CoreUserProfileView.SocialActionFavouriteList.as_view(), name='favourite-list'),
    url(r'^desfavoritar/$', CoreUserProfileView.SocialActionRemoveFavourite.as_view(), name='unfavourite'),
    url(r'^sugestoes/$', CoreUserProfileView.SocialActionSuggest.as_view(), name='suggest'),
    url(r'^sugestoes/list/$', CoreUserProfileView.SocialActionSuggestList.as_view(), name='suggestList'),

    url(r'^remover-sugestao/$', CoreUserProfileView.SocialActionRemoveSuggest.as_view(), name='unsuggest'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', CoreUserProfileView.CoreUserProfile.as_view(), name='show'),
    # url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', views.ProfileShowView.as_view(), name='show'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/$', views.ProfileFollowingsView.as_view(), name='followings'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/search/$', CoreUserProfileView.CoreProfileFollowingsSearch.as_view(), name='followings-search'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/search/list/$', CoreUserProfileView.CoreProfileFollowingsSearchList.as_view(), name='followings-search-list'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/load/ajax/$', CoreUserProfileView.CoreProfileFollowingsLoadAjax.as_view(), name='followings-load-ajax'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', views.ProfileFollowersView.as_view(), name='followers'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/search/$', CoreUserProfileView.CoreProfileFollowersSearch.as_view(), name='followers-search'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/search/list/$', CoreUserProfileView.CoreProfileFollowersSearchList.as_view(), name='followers-search-list'),

    # url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/$', views.ProfileCommunitiesView.as_view(), name='communities'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/$', CoreUserProfileView.CoreProfileCommunitiesSearchView.as_view(), name='communities'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/list/$', CoreUserProfileView.CoreProfileCommunitiesSearchListView.as_view(), name='communities-list'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/load/ajax/$', CoreUserProfileView.CoreProfileCommunitiesLoadAjax.as_view(), name='communities-load-ajax'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/$', CoreUserProfileView.CoreProfileVideosView.as_view(), name='videos'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/$', CoreUserProfileView.CoreProfileVideosSearch.as_view(), name='videos-search'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/list/$', CoreUserProfileView.CoreProfileVideosList.as_view(), name='videos-search-list'),

    url(r'^ajax/user/communities/$', CoreUserProfileView.CoreUserCommunitiesListAjax.as_view(), name='user-communities-ajax'),
]