from PIL import Image


def watermark_with_transparency(
        src,
        name,
        factor=0.3
):
    base_image = src
    watermark = Image.open("/app/resources/watermark.png")
    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    ww, wh = watermark.size
    watermark = watermark.resize((int(factor * ww), int(factor * wh)), Image.ANTIALIAS)
    transparent.paste(base_image, (0, 0))
    ww, wh = watermark.size
    transparent.paste(watermark, (width - ww - 30, height - wh - 30), mask=watermark)
    transparent.save(f"/app/static/{name}.png")
    thumbnail = transparent.resize((width//3, height//3))
    thumbnail.save(f"/app/static/{name}-thumbnail.png")

