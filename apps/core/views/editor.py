from ckeditor_uploader.views import get_upload_filename
from django.http import HttpResponse
from django.views import generic
from ckeditor_uploader import image_processing
from ckeditor_uploader import utils
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django_thumbor import generate_url

__author__ = 'phillip'


class ImageUploadView(generic.View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        """
        Uploads a file and send back its URL to CKEditor.
        """
        uploaded_file = request.FILES['upload']

        print request.GET

        backend = image_processing.get_backend()
        self._verify_file(backend, uploaded_file)
        saved_path = self._save_file(request, uploaded_file)
        self._create_thumbnail_if_needed(backend, saved_path)
        url = utils.get_media_url(saved_path)

        # Respond with Javascript sending ckeditor upload url.
        return HttpResponse("""
        <script type='text/javascript'>
            window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
        </script>""".format(request.GET['CKEditorFuncNum'], url))

    def _verify_file(self, backend, uploaded_file):
        try:
            backend.image_verify(uploaded_file)
        except utils.NotAnImageException:
            return self._on_verification_failure()

    def _on_verification_failure(self):
        pass

    @staticmethod
    def _save_file(request, uploaded_file):
        filename = get_upload_filename(uploaded_file.name, request.user)
        saved_path = default_storage.save(filename, uploaded_file)
        return saved_path

    @staticmethod
    def _create_thumbnail_if_needed(backend, saved_path):
        if backend.should_create_thumbnail(saved_path):
            backend.create_thumbnail(saved_path)


upload = csrf_exempt(ImageUploadView.as_view())