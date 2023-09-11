from rest_framework.exceptions import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if "https://www.youtube.com/" in tmp_val:
            return True
        else:
            raise ValidationError('This is not a video link')
