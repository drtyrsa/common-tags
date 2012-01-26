=========================
Common tags
=========================

A set of simple template tags for Django. Feel free to override templates for inclusion tags (while templates provided are ready to use too). This fork of django-meio-easytags - https://github.com/drtyrsa/django-meio-easytags - is required.

render_form (inclusion tag)
---------------------------
Renders a form::
        
    {% render_form form [method='post'] [submit_text=''] [action=''] class_name=[''] id=[''] [no_csrf=0] %}

Template used: ``render_form.html``

Arguments:

* ``form`` - form object to render
* ``method`` - ``method`` attribute of ``<form>`` tag. If equals to ``'inner'`` ``<form>`` tags and submit button are not rendered.
* ``submit_text`` - a text on submit button. If there is no ``submit_text`` provided, a button is not rendered.
* ``action`` - ``action`` attribute of ``<form>`` tag
* ``class_name`` - ``class_name`` attribute of ``<form>`` tag
* ``id`` - ``id`` attribute of ``<form>`` tag
* ``no_csrf`` - if evaluates to ``True``, csrf token is not rendered.

render_field (inclusion tag)
----------------------------
Renders a form field.::
        
    {% render_field field %}

Template used: ``render_field.html``

Arguments:

* ``field`` - a field to render

field_label (inclusion tag)
---------------------------
Renders a field's label. If the filed is required, renders an asterisk after::
        
    {% field_label field %}

Template used: ``field_label.html``

Arguments:

* ``field`` - a field with a label to render

submit_button (inclusion tag)
-----------------------------
Renders submit button with given ``text``. If ``no_fieldset`` evaluates to ``False``, ``<button>`` tag is surrounded by ``<filedset>`` tag.::
        
    {% submit_button text [no_fieldset=0] %}

Template used: ``submit_button.html``

Arguments:

* ``field`` - a field with a label to render
* ``no_fieldset`` - if evaluates to ``False``, ``<button>`` tag is surrounded by ``<filedset>`` tag.

render_messages (inclusion tag)
-------------------------------
Renders a messages list::
        
    {% render_messages messages %}

Template used: ``render_messages.html``

Arguments:

* ``messages`` - messages list to render

smart_date (filter)
-------------------
Converts given datetime to human(Russian)-readable format.::
    
    {{ today_date|smart_date }} -> outputs time, e. g. '12:34'
    {{ yesterday_date|smart_date }} -> outputs 'Вчера'
    {{ this_year_date|smart_date }} -> outputs e. g. '23&nbsp;февраля'
    {{ not_this_year_date|smart_date }} -> outputs e. g. '23.02.1988'

page_title (tag)
-----------------
Outputs given string and saves it {{ page_title }} context variable. The variable will be accessible from in every template block. There is a common task to output page title in ``<title>`` tag and in ``<h1>`` tag. This tag allows to solve this task DRY and clean.::
    
    {% block title %}
        {% page_title 'Contacts' %}
    {% endblock %}
    
    {% block content %}
        {{ page_title }}
    {% endblock %}

This code will output ``'Contacts'`` twice.