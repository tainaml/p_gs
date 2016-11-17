from apps.article.models import Article
from rede_gsti.celery import app
import bleach
import re


@app.task
def clean_article_links(article_id):

    portal_rule = re.compile(r'http(.+)(portalgsti\.com\.br)')

    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        print("ERROR: Article does not exist")
        return
    except Exception as e:
        print("ERROR: General error on get article. [{}]".format(e))
        return

    def no_follow_external_links(attrs, new=False):

        _href = attrs.get('href')

        if _href and _href[0:4] == 'http' and not portal_rule.match(_href):
            attrs['rel'] = 'nofollow'

        return attrs

    article_text = bleach.linkify(
        text=article.text,
        callbacks=[
            no_follow_external_links
        ]
    )

    if article_text != article.text:
        article.text = article_text
        article.save()
