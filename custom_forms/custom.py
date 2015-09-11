from django import forms

class AbstractIdeiaForm(object):
    def process(self):
        try:
            return self.__process__() if self.is_valid() else False
        except NotImplementedError:
            raise NotImplementedError
        except Exception, e:
            print e.message
            self.add_error(None, "General error!")
            return False

    def __process__(self):
        raise NotImplementedError

    def is_valid(self):
        raise NotImplementedError

    def add_error(self, *args, **kwargs):
        raise NotImplementedError

class IdeiaForm(forms.Form, AbstractIdeiaForm):
    def __init__(self, *args, **kwargs):
        super(IdeiaForm, self).__init__(*args, **kwargs)



class IdeiaModelForm(forms.ModelForm, AbstractIdeiaForm):

    def __init__(self, *args, **kwargs):
        super(IdeiaModelForm, self).__init__(*args, **kwargs)