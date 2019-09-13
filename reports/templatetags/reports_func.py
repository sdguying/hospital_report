from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.simple_tag
def get_img_url(img):
    """图片地址"""
    image_path = '/images/reports/' + str(img.id) + '.svg'
    return static(image_path)


# @register.filter
# def filter_owner(value, request):
#     if value.owner_id == request.user.id:
#         pass
#     else:
#         value.delete()
#     return value
