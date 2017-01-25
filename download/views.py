from django.shortcuts import render
from django.views import generic
from django.template.defaultfilters import filesizeformat
import pafy
# Create your views here.


class Download(generic.View):
    template_name = 'download/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        url = request.POST['url']
        video = pafy.new(url)
        stream = video.streams
        l = list()
        for s in stream:
            l.append([s.resolution, s.extension, filesizeformat(s.get_filesize()), s.url])
        return render(request, self.template_name, {'title': video.title, 'streams': l, 'desc': video.description,
                                                    'likes': video.likes, 'dislikes': video.dislikes,
                                                    'thumb': video.thumb, 'duration': video.duration,
                                                    'views': video.viewcount})
