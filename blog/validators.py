from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size_mb = 5
    if image.size > max_size_mb * 1024 * 1024:
        error_message = f"圖片大小不得超過 {max_size_mb}MB"
        raise ValidationError(error_message)
