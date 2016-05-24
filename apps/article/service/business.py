from ..models import Article
from django.template.defaultfilters import slugify

def get_valid_slug(instance, pre_slug):
    slug = slugify(pre_slug)

    # TODO criteria with month and year
    article_with_this_slug = Article.objects.filter(slug=slug)
    if article_with_this_slug:
        slug+="-" + str(instance.id or 1)
        return get_valid_slug(instance, slug)

    return slug


def get_article(article_id=None):

    article = Article()

    if article_id:
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return False

    return article


def create_temp_article(author):
    article = Article()
    article.author = author
    article.status = Article.STATUS_TEMP
    article.save()
    return article


def save_article(article, data):
    saved = article.save()
    return False if saved is False else article


def delete_article(article):
    article.status = article.STATUS_TRASH
    return article.save()


def count_articles(author):
    try:
        count = Article.objects.filter(author=author, status=Article.STATUS_PUBLISH).count()
    except:
        return 0

    return count


def get_articles_by_user(author):
    try:
        articles = Article.objects.get(author=author)
    except Article.DoesNotExist:
        articles = False

    return articles
