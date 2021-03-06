from django.db import models
from django.conf import settings


class ContactSubject(models.Model):

    title = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.title


class Contact(models.Model):

    # case user aren't member of social network
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)

    # case user are member of social network
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    subject = models.ForeignKey(ContactSubject, null=False)
    message = models.CharField(max_length=1024, blank=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, blank=False)

    @property
    def email(self):
        if self.author:
            return self.author.email
        else:
            return self.contact_email

    @property
    def name(self):
        if self.author:
            return self.author.get_full_name()
        else:
            return self.contact_name

    def __unicode__(self):
        return (self.message[:100] + "... " ) or "no message " + "(%s)" % self.subject.title
