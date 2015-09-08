from django import forms


class IdeiaForm(forms.Form):

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


class IdeiaModelForm(forms.ModelForm, IdeiaForm):

    def __init__(self, *args, **kwargs):
        super(IdeiaModelForm, self).__init__(*args, **kwargs)