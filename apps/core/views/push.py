from django.forms import modelform_factory
from django.http import JsonResponse
from django.views import View
from push_notifications.models import GCMDevice
import copy



class ReceiveSubscribe(View):



    def get(self, request):

        data = copy.copy(dict(request.GET))
        instance = None
        if 'registration_id' in data:
            if type(data['registration_id']) == list:
                data['registration_id'] = data['registration_id'][0]

            try:
                instance = GCMDevice.objects.get(registration_id=data['registration_id'])
            except GCMDevice.DoesNotExist, GCMDevice.MultipleObjectsReturned:
                pass


        Form = modelform_factory(model=GCMDevice, fields=('registration_id', 'user', 'cloud_message_type'))


        data.update({
            'user': request.user.id if request.user.is_authenticated() else None,
            'cloud_message_type': 'FCM'

        })

        print data, request.user.is_authenticated
        form = Form(data=data, instance=instance)

        if form.is_valid():
            form.save()

        else:
            print form.errors

        return JsonResponse(data={})