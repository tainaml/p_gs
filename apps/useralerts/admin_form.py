from django import forms
from ideia_summernote.widget import SummernoteWidget
from models import UserAlert


class UserAlertForm(forms.ModelForm):


    class Media:
        js = (
            # 'https://code.jquery.com/jquery-2.2.4.min.js',
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.min.js', )

        css= {
            'all': (
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.css',
            )
        }

    class Meta:
        model = UserAlert
        exclude = ()
        widgets = {
            'content': SummernoteWidget(editor_conf='article')
        }