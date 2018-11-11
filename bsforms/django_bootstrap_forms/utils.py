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

from django.conf import settings
from django.utils import six
from django.forms import CheckboxInput
from django.forms import RadioSelect

_bsforms_settings = getattr(settings, 'BOOTSTRAP_FORMS', {})


def update_css_classes(orig, add):
    if isinstance(add, six.string_types):
        add = add.split()

    return list(orig) + [e for e in add if e not in orig]


def get_label_classes(field, extra_classes):
    """Get CSS classes for a label.

    This merges classes from:

    #. settings.BOOTSTRAP_FORMS.label_classes
    #. widget.get_label_classes
    #. form.get_label_classes
    #. extra_classes
    """
    form = field.form
    widget = field.field.widget

    classes = set(_bsforms_settings.get('label_classes', set()))
    if hasattr(widget, 'get_label_classes'):
        classes |= widget.get_label_classes()
    if hasattr(form, 'get_label_classes'):
        classes |= form.get_label_classes()

    if isinstance(extra_classes, six.string_types):
        classes |= set(extra_classes.split())
    elif isinstance(extra_classes, (list, tuple)):
        classes |= set(extra_classes)
    else:
        classes |= extra_classes  # should be a set

    return classes


def get_label_attrs(field, extra_attrs=None):
    """Get attributes for a label.

    This merges attributes from:

    #. widget.get_label_attrs
    #. form.get_label_attrs
    #. settings.BOOTSTRAP_FORMS.label_attrs
    #. extra_attrs

    .. and adds the mandatory "for" attribute.

    Note that the attributes from settings are applied *after* the attributes comming from widget and form, so
    that somebody using this app can overwrite any attribute.
    """
    if extra_attrs is None:
        extra_attrs = {}

    form = field.form
    widget = field.field.widget

    label_attrs = {}
    if hasattr(widget, 'get_label_attrs'):
        label_attrs.update(widget.get_label_attrs())
    if hasattr(form, 'get_label_attrs'):
        label_attrs.update(form.get_label_attrs())

    label_attrs.update(_bsforms_settings.get('label_attrs', {}))
    label_attrs.update(extra_attrs)

    label_attrs['for'] = field.id_for_label
    return label_attrs


def get_label_context(field, extra_context=None):
    if extra_context is None:
        extra_context = {}

    form = field.form
    widget = field.field.widget
    ctx = {}

    if hasattr(widget, 'get_label_context'):
        ctx.update(widget.get_label_context())
    if hasattr(form, 'get_label_context'):
        ctx.update(form.get_label_context())
    ctx.update(_bsforms_settings.get('label_context', {}))
    ctx.update(extra_context)
    return ctx


def label(boundfield, horizontal='', size='', sronly=False, extra_context=None):
    if extra_context is None:
        extra_context = {}
    widget = boundfield.field.widget

    extra_classes = extra_context.get('attrs', {}).pop('class', '')
    classes = get_label_classes(boundfield, extra_classes=extra_classes)

    if isinstance(widget, (CheckboxInput, RadioSelect)) or getattr(widget, 'is_checkbox', False):
        classes.add('form-check-label')

    # handle special parameters
    if horizontal:
        classes |= set(horizontal.split())
        classes.add('col-form-label')
    if size:
        classes.add('col-form-label-%s' % size)
    if sronly:
        classes.add('sr-only')

    attrs = get_label_attrs(boundfield, extra_attrs=extra_context.pop('attrs', {}))
    attrs['class'] = ' '.join(sorted(classes))

    context = dict(get_label_context(boundfield, extra_context=extra_context),
                   label=boundfield.label, attrs=attrs)

    # Get template name
    template_name = getattr(widget, 'label_template_name', None) or 'bootstrap_forms/label.html'

    return widget._render(template_name, context)
