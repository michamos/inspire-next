# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2013, 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""DOI field."""

from __future__ import absolute_import, division, print_function

from wtforms import StringField

from ..field_base import INSPIREField
from ..filter_utils import strip_prefixes, strip_string
from ..validation_utils import DOISyntaxValidator

__all__ = ['DOIField']


def missing_doi_warning(dummy_form, field, submit=False, fields=None):
    """
    Field processor.

    Checks for existence of a DOI, and otherwise asks people to provide it.
    """
    if not field.errors and not field.data:
        field.add_message("Please provide a DOI if possible.", state="warning")
        raise StopIteration()


class DOIField(INSPIREField, StringField):

    """DOIField."""

    def __init__(self, **kwargs):
        """Init."""
        defaults = dict(
            icon='barcode',
            validators=[
                DOISyntaxValidator(),
            ],
            filters=[
                strip_string,
                strip_prefixes("doi:", "http://dx.doi.org/"),
            ],
            placeholder="e.g. 10.1234/foo.bar...",
            widget_classes="form-control"
        )
        defaults.update(kwargs)
        super(DOIField, self).__init__(**defaults)
