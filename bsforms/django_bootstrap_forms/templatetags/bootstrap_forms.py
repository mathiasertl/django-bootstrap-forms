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

from ..utils import label

register = template.Library()


@register.simple_tag(takes_context=True, name='label')
def label_tag(context, field, horizontal='', size='', sronly=False, **attrs):
    # get anything from the context
    horizontal = horizontal or context.get('form_horizontal_label', '')
    size = size or context.get('form_size', '')
    sronly = sronly or context.get('form_sronly', '')

    return label(field, horizontal=horizontal, size=size, sronly=sronly,
                 extra_context={'attrs': attrs})
