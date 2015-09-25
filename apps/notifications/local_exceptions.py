__author__ = 'phillip'

class NotValidNotificationSettings(Exception):
    def __init__(self, value, setting_name):
        self.value = value
        self.setting_name = setting_name

    def __unicode__(self):
        return "Notification settings \"%s\" not found or is not a valid integer number. You need specify this setting." % self.setting_name + repr(self.value)
