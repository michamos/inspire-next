# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2016 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction

"""API of Author records."""

from __future__ import absolute_import, division, print_function

import json

from inspirehep.modules.records.serializers.response import (
    record_responsify_nocache,
)
from inspirehep.modules.search import LiteratureSearch

from ..utils import build_citesummary, get_id


class APIAuthorsCitesummary(object):

    """Implementation of citesummary for Author records."""

    def serialize(self, pid, record, links_factory=None):
        search_by_author = LiteratureSearch().query(
            'match', authors__recid=get_id(record)
        ).params(
            _source=[
                'authors.recid',
                'collaboration.value',
                'collections.primary',
                'control_number',
                'earliest_date',
                'facet_inspire_doc_type',
                'inspire_categories',
                'titles.title',
            ],
        )

        return json.dumps(build_citesummary(search_by_author))


citesummary = APIAuthorsCitesummary()
citesummary_response = record_responsify_nocache(
    citesummary, 'application/json')
