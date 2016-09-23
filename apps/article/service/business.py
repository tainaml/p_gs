from ..models import Article
from django.template.defaultfilters import slugify

def get_valid_slug(instance, pre_slug):
    slug = slugify(pre_slug)

    # TODO criteria with month and year
    try:
        article_with_this_slug = Article.objects.get(slug=slug)
        if article_with_this_slug and article_with_this_slug!=instance:
            slug+="-" + str(instance.id or 1)
            return get_valid_slug(instance, slug)
    except Article.DoesNotExist:
        pass

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
    if not article.first_slug:
        article.first_slug=article.slug

    # for key in data.keys():
    #     if not hasattr(article, key):
    #         continue
    #
    #     setattr(article, key, data.get(key))

    saved = article.save()
    return False if saved is False else article


def delete_article(article):
    article.status = article.STATUS_TRASH
    return article.save()


def count_articles(author):
    try:
        count = author.articles.filter(Article.STATUS_PUBLISH).count()
    except:
        return 0

    return count


def get_articles_by_user(author):
    try:
        articles = Article.objects.get(author=author)
    except Article.DoesNotExist:
        articles = False

    return articles
