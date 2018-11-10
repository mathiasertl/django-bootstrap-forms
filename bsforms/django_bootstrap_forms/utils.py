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

from django.utils import six


def update_css_classes(orig, add):
    if isinstance(add, six.string_types):
        add = add.split()

    return list(orig) + [e for e in add if e not in orig]
