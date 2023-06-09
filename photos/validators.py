from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 1048576:  # 1 MiB in bytes
        raise ValidationError("The maximum file size that can be uploaded is 1 MiB")
    else:
        return value
