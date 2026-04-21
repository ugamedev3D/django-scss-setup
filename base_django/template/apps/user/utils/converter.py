from django.http import JsonResponse
import requests
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

from core import settings

def resizeConverter(request, url):
    user = request.user
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # process user avatar Compression 
        buffer = process_buffer(response.content)

        file_name = f"user_{user.id}.webp"
        
        if user.avatar:
            user.avatar.delete(save=False)

        user.avatar.save(file_name, ContentFile(buffer.read()), save=True)
                
    except Exception as e:
        print("Avatar error:", e)

def process_buffer(image_file, size = settings.allauth.AVATAR_SIZE, quality =  settings.allauth.AVATAR_QUALITY):
    img = Image.open(BytesIO(image_file))
    # To fix the orientation for mobile upload
    img = ImageOps.exif_transpose(img)

    # check if the alpha is exits
    has_alpha = img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info
    )

    img = img.convert("RGBA") if has_alpha else img.convert("RGB")

    img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)

    buffer = BytesIO()

    img.save(
        buffer,
        format="WEBP",
        quality=quality,
        optimize=True,
        method=6,
        lossless=has_alpha
    )
    buffer.seek(0)
    return buffer


