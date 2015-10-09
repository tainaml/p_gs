from django.conf.urls import url
from apps.userprofile import views
from ..views import user as CoreUserProfileView

urlpatterns = [

    url(r'^edit/$', views.ProfileEditView.as_view(), name='edit'),
    url(r'^ajax/edit/$', CoreUserProfileView.CoreProfileEditAjax.as_view(), name='edit-ajax'),

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

    url(r'^feed/$', CoreUserProfileView.CoreUserFeed.as_view(), name='user_feed'),

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', views.ProfileShowView.as_view(), name='show'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/$', views.ProfileFollowingsView.as_view(), name='followings'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', views.ProfileFollowersView.as_view(), name='followers'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/communities/$', views.ProfileCommunitiesView.as_view(), name='communities'),

]