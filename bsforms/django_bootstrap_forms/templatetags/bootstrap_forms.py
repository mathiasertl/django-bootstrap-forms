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

from django import template
from django.conf import settings

from ..utils import update_css_classes

register = template.Library()


@register.inclusion_tag(['label.html', 'bootstrap_forms/label.html'], takes_context=True)
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
