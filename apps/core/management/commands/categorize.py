from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db.models import Q
from apps.article.models import Article
from apps.community.models import Community
from apps.feed.models import FeedObject


class Command(BaseCommand):

    def handle(self, *args, **options):
        communities = Community.objects.all()


        for community in communities:

            if community.title.lower() in ['mais', 'desenvolvimento', 'infraestrutura', 'design', 'mobile', 'ios', 'cores', 'branding', 'processo criativo']:
                print community.title
            else:
                criteria = Q(title__unaccent__icontains=community.title+" ") | Q(text__unaccent__icontains=" " + community.title)

                articles  = Article.objects.filter(criteria)
                for article in articles:
                    feed = FeedObject.objects.get(content_type=ContentType.objects.filter(model='article'), object_id=article.id)
                    feed.taxonomies.add(community.taxonomy)
                    feed.communities.add(community)
                    feed.save()
                    print "Done article %s" % article.title

















