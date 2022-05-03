from django import template

register = template.Library()


@register.filter
def distinct_size(size_list):
    all_sizes = ['XS', 'S', 'M', 'L', 'XL']
    sizes = [item.size.upper() for item in size_list if item.item_count > 0]
    unique_sizes = list(set(sizes))
    return [s.upper() for s in all_sizes if s in unique_sizes]