from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = "public-read"

    def __init__(self, *args, **kwargs):
        kwargs["custom_domain"] = settings.AWS_CLOUDFRONT_DOMAIN
        super(PublicMediaStorage, self).__init__(*args, **kwargs)
