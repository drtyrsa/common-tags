# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase
from django.template import Context, Template
from django import forms
from django.contrib.messages.storage.base import Message, constants


class TestCommonTags(TestCase):
    def _render_template(self, template_str, context):
        template = Template(template_str)
        context = Context(context)
        return template.render(context)

    def setUp(self):
        class SampleForm(forms.Form):
            name = forms.CharField(max_length=20, label=u'You name', help_text=u'Real name, please')
            age = forms.IntegerField(label=u'Your age', initial=10, required=False)
            agreed = forms.BooleanField(label=u'I am agreed')
            hid = forms.CharField(widget=forms.HiddenInput, max_length=20)
        self.form = SampleForm()

    def test_checkbox_or_radio(self):
        template_str = '''
            {% load common_tags %}
            {% if field|checkbox_or_radio %}112233{% else %}009988{% endif %}
        '''
        out = self._render_template(template_str, {'field': self.form['name']})
        self.assertTrue('009988' in out)

        out = self._render_template(template_str, {'field': self.form['agreed']})
        self.assertTrue('112233' in out)

    def test_field_label(self):
        template_str = '''
            {% load common_tags %}
            {% field_label field %}
        '''
        out = self._render_template(template_str, {'field': self.form['name']})
        self.assertTrue('<span class="required">' in out)

        out = self._render_template(template_str, {'field': self.form['age']})
        self.assertFalse('<span class="required">' in out)

    def test_submit_button(self):
        template_str = '''
            {% load common_tags %}
            {% submit_button 'submit' %}
        '''
        out = self._render_template(template_str, {})
        self.assertEqual('<fieldset><button class="submit_button" type="submit">submit</button></fieldset>', out.strip())

        template_str = '''
            {% load common_tags %}
            {% submit_button 'submit' no_fieldset=1 %}
        '''
        out = self._render_template(template_str, {})
        self.assertEqual('<button class="submit_button" type="submit">submit</button>', out.strip())

    def test_render_messages(self):
        template_str = '''
            {% load common_tags %}
            {% render_messages messages %}
        '''
        out = self._render_template(template_str, {})
        self.assertFalse(bool(out.strip()))

        out = self._render_template(template_str, {'messages': ['abc']})
        self.assertTrue('<ul class="messages">' in out)
        self.assertTrue('<li>abc</li>' in out)

        msg = Message(constants.INFO, 'abc')
        out = self._render_template(template_str, {'messages': [msg]})
        self.assertTrue('<li class="info">abc</li>' in out)

    def test_render_field(self):
        template_str = '''
            {% load common_tags %}
            {% render_field field %}
        '''
        out = self._render_template(template_str, {'field': self.form['name']})
        self.assertTrue('<label for="id_name" class="field_label">You name<span class="required">*</span></label>' in out)
        self.assertTrue('<input id="id_name" type="text" name="name" maxlength="20" />' in out)
        self.assertTrue('<span class="help_text">Real name, please</span>' in out)
        self.assertTrue('<fieldset>' in out)

        out = self._render_template(template_str, {'field': self.form['agreed']})
        self.assertTrue('<input type="checkbox" name="agreed" id="id_agreed" />&nbsp;<label for="id_agreed" class="field_label_inline">I am agreed<span class="required">*</span></label>' in out)
        self.assertTrue('<fieldset>' in out)

    def test_render_field_no_fieldset(self):
        template_str = '''
            {% load common_tags %}
            {% render_field field no_fieldset=1 %}
        '''
        out = self._render_template(template_str, {'field': self.form['name']})
        self.assertFalse('<fieldset>' in out)

        out = self._render_template(template_str, {'field': self.form['agreed']})
        self.assertFalse('<fieldset>' in out)

    def test_render_form_no_kwargs(self):
        template_str = '''
            {% load common_tags %}
            {% render_form form %}
        '''
        out = self._render_template(template_str, {'form': self.form})
        self.assertTrue('<form action="" method="post" class="main_form">' in out)
        self.assertFalse('submit' in out)

    def test_render_form_with_kwargs(self):
        template_str = '''
            {% load common_tags %}
            {% render_form form method='get' submit_text='submit me' action='http:/google.com' class_name='my_class' id='my_id' no_csrf=1 %}
        '''
        out = self._render_template(template_str, {'form': self.form})
        self.assertTrue('<form action="http:/google.com" method="get" class="my_class" id="my_id">' in out)
        self.assertTrue('<button class="submit_button" type="submit">submit me</button>' in out)

    def test_render_form_hidden_fields(self):
        template_str = '''
            {% load common_tags %}
            {% render_form form %}
        '''
        out = self._render_template(template_str, {'form': self.form})
        self.assertTrue('<input type="hidden" name="hid" id="id_hid" />' in out)

    def test_smart_date_today(self):
        template_str = '''
            {% load common_tags %}
            {{ date|smart_date }}
        '''
        date = datetime.today()
        out = self._render_template(template_str, {'date': date})
        self.assertTrue(date.strftime('%H:%M') in out)

    def test_smart_date_yesterday(self):
        template_str = '''
            {% load common_tags %}
            {{ date|smart_date }}
        '''
        date = datetime.today() - timedelta(days=1)
        out = self._render_template(template_str, {'date': date})
        self.assertTrue(u'Вчера' in out)

    def test_smart_date_this_year(self):
        template_str = '''
            {% load common_tags %}
            {{ date|smart_date }}
        '''
        date = datetime.today()
        if date.month == 1:
            date = date.replace(month=3)
            month_str = u'марта'
        else:
            date = date.replace(month=1)
            month_str = u'января'
        out = self._render_template(template_str, {'date': date})
        self.assertTrue(('%d&nbsp;%s' % (date.day, month_str)) in out)

    def test_smart_date_not_this_year(self):
        template_str = '''
            {% load common_tags %}
            {{ date|smart_date }}
        '''
        date = datetime.today()
        date = date.replace(year=date.year - 1)
        out = self._render_template(template_str, {'date': date})
        self.assertTrue(date.strftime(u'%d.%m.%Y') in out)

    def test_page_title(self):
        template_str = '''
            {% load common_tags %}
            {% block one %}{% page_title 'doremi' %}{% endblock %}{% block two %}{{ page_title }}{% endblock %}
        '''
        out = self._render_template(template_str, {})
        self.assertTrue('doremidoremi' in out)