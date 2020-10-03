from django import forms
from django.core.exceptions import ValidationError


class DownloadForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control input-lg", "placeholder": "Paste the URL of YouTube video here...."}), label='')

    def clean_url(self):
        url = self.cleaned_data['url']
        # to support share url
        if 'youtu.be' in url:
            video_id = url.split('/')[-1]
            url = 'https://www.youtube.com/watch?v=' + video_id
            print(video_id, url)

        # to support mobile YouTube url
        if 'm.' in url:
            url = url.replace('m.', '')

        if len(url.split("=")[-1]) != 11:  # Checks whether the url contains the 11 character unique video id
            raise ValidationError("Incorrect YouTube video URL")

        return url
