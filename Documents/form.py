# forms.py
from django import forms
from multiupload.fields import MultiFileField


class UploadForm(forms.Form):
    Documents = MultiFileField(min_num=1, max_num=3)

    # If you need to files media files, you can use this:
    Documents = MultiFileField(
        min_num=1,
        max_num=1000,
        # max_file_size=1024*1024*5,
    )