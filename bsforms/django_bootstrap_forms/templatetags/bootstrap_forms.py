# -*- coding: utf-8 -*-
#
# This file is part of django-bootstrap-forms (https://github.com/mathiasertl/django-bootstrap-forms).
#
# django-bootstrap-forms is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# django-bootstrap-forms is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with django-bootstrap-forms.  If
# not, see <http://www.gnu.org/licenses/>.

import functools
from inspect import getfullargspec

from django import template
from django.template.library import TagHelperNode
from django.template.library import parse_bits
from django.conf import settings

from ..utils import update_css_classes

register = template.Library()


class BootstrapFormsInclusionNode(TagHelperNode):
    def __init__(self, func, takes_context, args, kwargs, filename):
        super().__init__(func, takes_context, args, kwargs)
        self.filename = filename

    def render(self, context):
        resolved_args, resolved_kwargs = self.get_resolved_arguments(context)

        # TODO: we could make the field optional here
        _dict = self.func(*resolved_args, **resolved_kwargs)  # self.func == decorated function

        t = context.render_context.get(self)
        if t is None:
            t = context.template.engine.select_template(self.filename)

        new_context = context.new(_dict)
        # Copy across the CSRF token, if present, because inclusion tags are
        # often used for forms, and we need instructions for using CSRF
        # protection to be as simple as possible.
        csrf_token = context.get('csrf_token')
        if csrf_token is not None:
            new_context['csrf_token'] = csrf_token
        return t.render(new_context)


def bootstrap_forms_inclusion_tag(filename, func=None, takes_context=None, name=None):
    # adaption from template.library.Library.inclusion_tag a.k.a. "@register.inclusion_tag"
    def dec(func):
        params, varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(func)
        function_name = (name or getattr(func, '_decorated_function', func).__name__)

        @functools.wraps(func)
        def compile_func(parser, token):
            bits = token.split_contents()[1:]
            args, kwargs = parse_bits(
                parser, bits, params, varargs, varkw, defaults,
                kwonly, kwonly_defaults, takes_context, function_name,
            )
            return BootstrapFormsInclusionNode(
                func, takes_context, args, kwargs, filename,
            )
        register.tag(function_name, compile_func)
        return func
    return dec


#@register.inclusion_tag(['label.html', 'bootstrap_forms/label.html'], takes_context=True)
@bootstrap_forms_inclusion_tag('label.html', takes_context=True)
def label(context, field, **attrs):
    label_attrs = getattr(settings, 'BOOTSTRAP_FORMS', {}).get('label_attrs', {})
    css_classes = update_css_classes([], label_attrs.pop('class', ''))

    context_attrs = context.get('label_attrs', {})
    css_classes = update_css_classes(css_classes, context_attrs.pop('class', ''))
    label_attrs.update(context_attrs)

    if 'class' in attrs:
        css_classes = update_css_classes(css_classes, attrs.pop('class', ''))

    label_attrs.update(attrs)
    label_attrs['for'] = field.id_for_label
    label_attrs['class'] = ' '.join(css_classes)

    context = {
        'label': field.label,
        'attrs': label_attrs,
    }
    return context
