import pafy
from django.views.generic import FormView
from .forms import DownloadForm


class IndexView(FormView):
    template_name = 'download/index.html'
    form_class = DownloadForm

    def form_valid(self, form):
        """If the form is valid, render to response"""
        url = form.cleaned_data.get("url")
        video = pafy.new(url)  # creates a pafy object for a given youtube url
        video.embed_url = pafy.g.urls["embed"] % (video.videoid,)
        # insert video object into the context
        context = self.get_context_data(form=form, video=video)
        return self.render_to_response(context)
