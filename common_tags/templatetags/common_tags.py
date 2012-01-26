# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from easytags import EasyLibrary
from django.utils.safestring import mark_safe


register = EasyLibrary()

def render_form(context, form, method='post', submit_text='', action='',
                class_name='', id='', no_csrf=False):
    '''
    Tag for form rendering. If the ``method`` is ``inner``, ``<form></form>``
    tags and submit button are not rendered.
    '''
    return {'form': form,
            'method': method,
            'submit_text': submit_text,
            'action': action,
            'class_name': class_name,
            'id': id,
            'no_csrf': no_csrf}
register.easyinctag(render_form, template_name='common_tags/render_form.html', takes_context=True)

def render_messages(context, messages):
    '''
    Tag for messages rendering.
    '''
    return {'messages': messages}
register.easyinctag(render_messages, template_name='common_tags/render_messages.html')

@register.filter('checkbox_or_radio')
def checkbox_or_radio(field):
    '''
    Test whether field's widget is ``CheckboxInput`` or ``RadioInput``
    '''
    return field.field.widget.__class__.__name__ in ('CheckboxInput', 'RadioInput')

def field_label(context, field):
    '''
    Renders field's label and asterix if the filed is required.
    '''
    return {'field': field}
register.easyinctag(field_label, template_name='common_tags/field_label.html')

def submit_button(context, text, no_fieldset=False):
    '''
    Renders submit button, if ``no_fieldset`` is ``False`` ``<button>`` tag
    is surrounded by ``<filedset>`` tag.
    '''
    return {'text': text, 'no_fieldset': no_fieldset}
register.easyinctag(submit_button, template_name='common_tags/submit_button.html')

def render_field(context, field):
    '''
    Renders one form field: input, errors, help_text, etc.
    '''
    return {'field': field}
register.easyinctag(render_field, template_name='common_tags/render_field.html')

def smart_date(date):
    '''
    Outputs date in human(Russian)-readable format.
    '''
    if date.date() == datetime.today().date():
        return date.strftime('%H:%M')
    if date.date() == (datetime.today() - timedelta(days=1)).date():
        return u'Вчера'
    if date.year == datetime.today().year:
        months = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня',
                  u'июля', u'августа', u'сентября', u'октября',
                  u'ноября', u'декабря')
        return mark_safe('%d&nbsp;%s' % (date.day, months[date.month - 1]))
    return date.strftime(u'%d.%m.%Y')
register.filter(smart_date)

def page_title(context, title):
    '''
    Outputs ``title`` and adds ``{{ page_title }}`` variable to global context.
    It will be accessible from any template block.
    '''
    context.dicts[0]['page_title'] = title
    return title
register.easytag(page_title)