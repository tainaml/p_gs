from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import contact as CoreContactViews

urlpatterns = [
    # Translators: URL de criacao de contato
    url(_(r'^$'), CoreContactViews.CoreContactView.as_view(), name='create'),

    # Translators: URL de atualizacao de contato
    url(_(r'^save/$'), CoreContactViews.CoreContactSaveViews.as_view(), name='save'),

    # Translators: URL de atualizacao de contato
    url(_(r'^contact-success/$'), CoreContactViews.CoreContactSuccessView.as_view(), name='success'),

]