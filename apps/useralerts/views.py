from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from models import UserAlert


class Show(View):

    alert = None
    context = {}

    def raise_404(self):
        raise Http404("User alert does not exist")

    def check_alert(self, id, request):
        try:
            self.alert = UserAlert.objects.get(id=id)
        except UserAlert.DoesNotExist, e:
            self.raise_404()
        except Exception, e:
            self.raise_404()

        if request.user not in self.alert.users.all():
            self.raise_404()

    def get(self, request, alert_id):
        self.check_alert(alert_id, request)

        self.context.update({
            'alert': self.alert
        })

        return render(request, 'useralerts/single.html', context=self.context)
