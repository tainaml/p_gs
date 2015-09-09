__author__ = 'phillip'


class NotFoundSocialSettings(Exception):
    def __init__(self, value, setting_name):
        self.value = value
        self.setting_name = setting_name

    def __unicode__(self):
        return "Social settings \"%s\" not found. You need specify this setting." % self.setting_name + repr(self.value)
