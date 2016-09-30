from django.conf.urls import url
from django.views.generic import RedirectView
HOME_INDEX_REDIRECT = RedirectView.as_view(pattern_name='index', permanent=True)
urls_old = [

    url(r'p/portalgsti.html', RedirectView.as_view(pattern_name='core:about', permanent=True)),
    url(r'p/cadastro-cancelado-com-sucessovoce-nao_11.html', HOME_INDEX_REDIRECT),
    url(r'p/fernando-palma.html', RedirectView.as_view(pattern_name='profile:show', permanent=True), {'username': "fernandopalma"}),
    url(r'p/botao-provisorio-certificacao-itil.html', HOME_INDEX_REDIRECT),
    url(r'p/pague-com-pagseguro-e-rapido-gratis-e.html', HOME_INDEX_REDIRECT),
    url(r'p/concursos-de-ti-em-aberto_1109.html', RedirectView.as_view(pattern_name='community:show', permanent=True), {'community_slug': "concursos"}),
    url(r'p/cursos-gratuitos-online-no-portal-gsti_27.html', RedirectView.as_view(pattern_name='community:show', permanent=True), {'community_slug': "cursos-gratuitos"}),
    url(r'p/downloads-e-ebooks-gratuitos.html', RedirectView.as_view(pattern_name='community:show', permanent=True), {'community_slug': "cursos-gratuitos"}),
    url(r'p/pagamento-certificacao-itil-foundation.html', HOME_INDEX_REDIRECT),
    url(r'p/pagamento-curso-itil-virtual-modulo.html', HOME_INDEX_REDIRECT),
    url(r'p/obrigado.html', HOME_INDEX_REDIRECT),
    url(r'p/obrigado_72.html', HOME_INDEX_REDIRECT),
    url(r'p/seu-e-mail-foi-retirado-da-turma-02.html', HOME_INDEX_REDIRECT),
    url(r'p/inscreva-se-no-treinamento-completo-de.html', HOME_INDEX_REDIRECT),
    url(r'p/inscrever-se.html', HOME_INDEX_REDIRECT),
    url(r'p/seu-e-mail-foi-confirmado-com-sucesso.html', HOME_INDEX_REDIRECT),
    url(r'p/reserva-efetuada-com-sucesso.html', HOME_INDEX_REDIRECT),
    url(r'p/guardamos-o-seu-e-mail-na-lista-de.html', HOME_INDEX_REDIRECT),
    url(r'p/precisamos-da-confirmacao-do-seu-e-mail.html', HOME_INDEX_REDIRECT),
    url(r'p/videos-e-video-aulas-de-ti-e-gestao.html', HOME_INDEX_REDIRECT),
    url(r'p/videos-e-video-aulas-de-ti-e-gestao.html', HOME_INDEX_REDIRECT),
    url(r'p/blog-page_27.html', HOME_INDEX_REDIRECT),
    url(r'p/obrigado_27.html', HOME_INDEX_REDIRECT),
    url(r'p/seu-e-mail-foi-registrado-para-proxima.html', HOME_INDEX_REDIRECT),
    url(r'p/segunda-turma-itil-virtual-com-fernando.html', HOME_INDEX_REDIRECT),
    url(r'p/inscricao-realizada-com-sucesso.html', HOME_INDEX_REDIRECT),
    url(r'p/blog-page_5.html', HOME_INDEX_REDIRECT),
    url(r'p/8888.html', HOME_INDEX_REDIRECT),
    url(r'p/seu-e-mail-foi-confirmado-com-suesso.html', HOME_INDEX_REDIRECT),
    url(r'p/voce-foi-inscrito-com-sucesso.html', HOME_INDEX_REDIRECT),
    url(r'p/downloads-e-ebooks-gratuitos.html', HOME_INDEX_REDIRECT),
    url(r'p/mapa-do-site-portal-gsti-onde-os.html', HOME_INDEX_REDIRECT),
    url(r'p/marcelo-gaspar.html', HOME_INDEX_REDIRECT),
    url(r'p/artigos.html', RedirectView.as_view(pattern_name='search:search-content', permanent=True), {'content_type': "articles"}),
    url(r'p/curso-itil-incompany.html', HOME_INDEX_REDIRECT),
    url(r'p/links.html', HOME_INDEX_REDIRECT),
    url(r'p/bruno-horta.html', RedirectView.as_view(pattern_name='profile:show', permanent=True), {'username': "brunohsoares"}),
    url(r'p/guia-completo-para-certificacao-iso.html', RedirectView.as_view(pattern_name='article:view', permanent=True), {'slug': "guia-completo-para-certificacao-iso-27002-foundation", 'year': "2013", 'month': '06'}),

]