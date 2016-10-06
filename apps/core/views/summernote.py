from django_thumbor import generate_url
import os
from ideia_summernote.views import Upload, check_sizes
from ideia_summernote.default import SUMMERNOTE_DEFAULT_CONFIG
from django.http import JsonResponse
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils.translation import ugettext as _
from ideia_summernote.local_exceptions import FileSizeNotSupported


class CoreUpload(Upload):

    SUMMERNOTE_SETTINGS =  getattr(settings, 'SUMMERNOTE_CONFIG', SUMMERNOTE_DEFAULT_CONFIG)
    MAXIMUM_SIZE = getattr(SUMMERNOTE_SETTINGS, 'maximum_image_upload', SUMMERNOTE_DEFAULT_CONFIG['maximum_image_upload'])

    is_user_authenticated = False

    def get_file_media_url(self, path, filename):
        media_url = os.path.join(settings.MEDIA_URL, path, filename)
        thumbor_media_url = generate_url(media_url, width=getattr(settings,'MAXIMUM_PC_IMAGE_WIDTH', 300))
        return thumbor_media_url

    def process_file(self, file, request):
        user_path=''

        if self.SUMMERNOTE_SETTINGS['use_path_user'] and self.is_user_authenticated:
            user_path = request.user.username

        filename = file.name
        ext = slugify(filename.split('.')[-1])
        name = slugify(".".join(filename.split('.')[0:-1]))
        filename = "{0}.{1}".format(name, ext)

        path = os.path.join(settings.MEDIA_ROOT, user_path, filename)
        path = default_storage.save(path, file)
        if path:
            return self.get_file_media_url(user_path, filename)

        return False


    def post(self, request):

        files = request.FILES
        urls = []

        self.is_user_authenticated = request.user.is_authenticated()
        if self.SUMMERNOTE_SETTINGS['restrict_to_user']:
            if not self.is_user_authenticated:
                return JsonResponse(data={'message': _('Only authenticated users can submit images!')}, status=403)

        if request.FILES:

            try:
                check_sizes(request.FILES)
            except FileSizeNotSupported:
                return JsonResponse(data={'message': _('File size not supported!')}, status=400)

            for file in files.values():
                processed_file = self.process_file(file, request)
                if processed_file:
                    urls.append(processed_file)

        return JsonResponse(data={'urls': urls})