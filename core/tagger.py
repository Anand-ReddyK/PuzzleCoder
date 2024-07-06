from django import template

register = template.Library()

'''
Creating a Custom tag to convert the _id into id 
'''
@register.simple_tag
def underscoreTag(obj, attribute):
    obj = dict(obj)
    return obj.get(attribute)