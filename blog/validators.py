from pathlib import Path

from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size_mb = 5
    if image.size > max_size_mb * 1024 * 1024:
        error_message = f"圖片大小不得超過 {max_size_mb}MB"
        raise ValidationError(error_message)


def validate_image_extension(image):
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    ext = Path(image.name).suffix.lower()

    if ext not in valid_extensions:
        error_message = f"不支援的檔案格式。支援的格式: {', '.join(valid_extensions)}"
        raise ValidationError(error_message)


def validate_image_dimensions(image):
    max_width = 800
    max_height = 600

    if image.width > max_width or image.height > max_height:
        error_message = f"圖片尺寸不符合目標尺寸: {max_width}x{max_height}, 目前尺寸: {image.width}x{image.height}"
        raise ValidationError(error_message)
