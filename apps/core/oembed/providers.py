from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import micawber
from micawber.providers import Provider


def get_providers():
    providers = micawber.bootstrap_noembed()

    # Custom Providers
    providers.register('http://(\S*.)?youtu(\.be/|be\.com/playlist)\S+', Provider('http://www.youtube.com/oembed'))
    providers.register('https://(\S*.)?youtu(\.be/|be\.com/playlist)\S+', Provider('http://www.youtube.com/oembed?scheme=https&'))

    return providers


def get_oembed_data_from_url(url):
    providers = get_providers()
    response = providers.request(url)
    html = response.get('html', '')
    html = html.replace('height="%d"' % response.get('height'), '')
    html = html.replace('width="%d"' % response.get('width'), 'style="width:100%; height:100%; position: absolute; top: 0; left: 0"')
    html = mark_safe(render_to_string('core/partials/responsive_embed.html', {'html': html}))
    return response.update({
        'html': html
    })