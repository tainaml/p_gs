from django.db.models import Sum
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from apps.core.models.rating import Rating


def update_rating(instance=None, exclude_instance=False):

    if instance and instance.course:
        course = instance.course.get()

        ratings = Rating.objects.filter(course=course)
        if exclude_instance:
            ratings = ratings.exclude(id=instance.id)

        reviews_sum = ratings.aggregate(Sum("value"))['value__sum']
        total_reviews = ratings.filter(course=course).count()

        reviews_sum = reviews_sum if reviews_sum else 0

        try:
            course.rating = reviews_sum/total_reviews
        except ZeroDivisionError:
            course.rating = 0

        course.save()


@receiver(post_save, sender=Rating)
def rating_created(sender, **kwargs):
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    update_rating(instance)

@receiver(pre_delete, sender=Rating)
def rating_deleted(sender, **kwargs):
    instance = kwargs['instance'] if 'instance' in kwargs else False
    if not instance:
        return

    update_rating(instance, exclude_instance=True)