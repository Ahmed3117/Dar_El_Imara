
from django import template

register = template.Library()

@register.filter
def withdrawn_counts(queryset):
    withdraw_sum = 0
    # paid_sum = 0
    for withdraw in queryset :
        withdraw_sum = withdraw_sum + withdraw.ammount
        # paid_sum = paid_sum + withdraw.price

    return {
    'withdraw_sum': withdraw_sum,
    # 'paid_sum': float(paid_sum) ,
    }
    
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)