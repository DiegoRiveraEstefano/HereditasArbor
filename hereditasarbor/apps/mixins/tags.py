from django.template.defaulttags import register

@register.filter(name='split')
def split(value, key): 
 
    value.split("key")
    return value.split(key)