from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
	return int(value) * int(arg)

@register.filter
def count(value):
	try:
		return(len(value))
	except:
		return False
