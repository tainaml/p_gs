from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.models.rating import Rating


def update_rating(instance=None):

    if instance and instance.course:
        course = instance.course.get()
        reviews_sum = Rating.objects.filter(course=course).aggregate(Sum("value"))['value__sum']
        total_reviews = Rating.objects.filter(course=course).count()
        course.rating = reviews_sum/total_reviews
        course.save()


@receiver(post_save, sender=Rating)
def rating_created(sender, **kwargs):
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    update_rating(instance)

@receiver(post_delete, sender=Rating)
def rating_deleted(sender, **kwargs):
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    update_rating(instance)