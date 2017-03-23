import pafy
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat
from django.views import generic


def url_corrector(url):
    # Converts the url to supported format if it's not in a format supported by pafy.
    correct_url = url

    if 'm.' in url:
        correct_url = correct_url.replace('m.', '')

    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
        correct_url = 'https://www.youtube.com/watch?v=' + video_id

    return correct_url


class Download(generic.View):
    """The view which handles the url and returns the download links."""

    template_name = 'download/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        url = request.POST['url']
        url = url_corrector(url)  # Converting the urls in a format that is supported by pafy.

        if len(url.split("=")[-1]) != 11:  # Checks whether the url contains the 11 character unique video id.
            return HttpResponse('Enter correct url.')

        video = pafy.new(url)  # creates a pafy object for a given youtube url.

        stream = video.streams  # both video and audio
        video_audio_streams = list()  # list of all the videos which also contain audio
        for s in stream:
            video_audio_streams.append(
                [s.resolution, s.extension, filesizeformat(s.get_filesize()), s.url + "&title=" + video.title])

        stream_video = video.videostreams  # only video
        video_streams = list()  # list of all the dash video formats(only video)
        for s in stream_video:
            video_streams.append(
                [s.resolution, s.extension, filesizeformat(s.get_filesize()), s.url + "&title=" + video.title])

        stream_audio = video.audiostreams  # only audio
        audio_streams = list()  # list of all the dash audio formats(only audio)
        for s in stream_audio:
            audio_streams.append(
                [s.resolution, s.extension, filesizeformat(s.get_filesize()), s.url + "&title=" + video.title])

        return render(request, self.template_name,
                      {'url': request.POST['url'], 'title': video.title, 'streams': video_audio_streams,
                       'desc': video.description, 'likes': video.likes,
                       'dislikes': video.dislikes, 'thumb': video.bigthumbhd,
                       'duration': video.duration, 'views': video.viewcount,
                       'stream_video': video_streams, 'stream_audio': audio_streams})
