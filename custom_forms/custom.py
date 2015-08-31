from django import forms


class IdeiaForm(forms.Form):

    def process(self):
        try:
            return self.__process__() if self.is_valid() else False
        except NotImplementedError:
            raise NotImplementedError
        except:
            self.add_error(None, "General error!")
            return False

    def __process__(self):
        raise NotImplementedError