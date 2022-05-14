from django import template

register = template.Library()


@register.filter
def change_comment_end(comments_count):
    final_version = f'{comments_count} '
    if str(comments_count).endswith('1') and comments_count != 11:
        final_version += 'ОТЗЫВ'
    elif str(comments_count)[-1] in ('234') and comments_count not in (12, 13, 14):
        final_version += 'ОТЗЫВА'
    else:
        final_version += 'ОТЗЫВОВ'
    return final_version