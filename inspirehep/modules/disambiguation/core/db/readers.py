# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Disambiguation core DB readers."""

from __future__ import absolute_import, division, print_function

from elasticsearch_dsl import Q
from sqlalchemy import type_coerce
from sqlalchemy.dialects.postgresql import JSONB

from invenio_records.models import RecordMetadata

from inspire_dojson.utils import get_recid_from_ref
from inspire_utils.record import get_value
from inspirehep.modules.search.api import LiteratureSearch
from inspirehep.utils.record import (
    get_abstract,
    get_collaborations,
    get_inspire_categories,
    get_keywords,
    get_title,
)

SIGNATURE_FIELDS = [
    'abstracts.value',
    'authors.affiliations.value',
    'authors.full_name',
    'authors.record',
    'authors.signature_block',
    'authors.uuid',
    'collaborations.value',
    'control_number',
    'inspire_categories.term',
    'keywords.value',
    'titles.title',
]


def get_all_curated_signatures():
    """Get all curated signatures from the DB.

    Walks through all Literature records and collects all signatures
    that were marked as curated in order to build the training set
    for ``BEARD``.

    Yields:
        dict: a curated signature.

    """
    query = RecordMetadata.query.with_entities(RecordMetadata.json).filter(
        type_coerce(RecordMetadata.json, JSONB)['_collections'].contains(['Literature']))

    for record in query.yield_per(1000):
        publication = _build_publication(record.json)
        for author in record.json.get('authors', []):
            if author.get('curated_relation'):
                yield _build_signature(author, publication)


def get_signatures_matching_a_phonetic_encoding(phonetic_encoding):
    """Get all signatures matching a phonetic encoding from ES.

    Args:
        phonetic_encodings(str): a phonetic encoding.

    Yields:
        dict: a signature matching the phonetic encoding.

    """
    query = Q('term', authors__signature_block__raw=phonetic_encoding)
    search_by_phonetic_encoding = LiteratureSearch().query('nested', path='authors', query=query)\
                                                    .params(_source=SIGNATURE_FIELDS, size=9999)

    for record in search_by_phonetic_encoding:
        record = record.to_dict()
        publication = _build_publication(record)
        for author in record.get('authors', []):
            if author['signature_block'] == phonetic_encoding:
                yield _build_signature(author, publication)


def _build_publication(record):
    return {
        'abstract': get_abstract(record),
        'authors': _get_authors_names(record),
        'collaborations': get_collaborations(record),
        'keywords': get_keywords(record),
        'publication_id': record['control_number'],
        'title': get_title(record),
        'topics': get_inspire_categories(record),
    }


def _build_signature(author, publication):
    return {
        'author_affiliation': _get_author_affiliation(author),
        'author_id': get_recid_from_ref(author.get('record')),
        'author_name': author['full_name'],
        'publication': publication,
        'publication_id': publication['publication_id'],
        'signature_block': author['signature_block'],
        'signature_uuid': author['uuid'],
    }


def _get_author_affiliation(author):
    return get_value(author, 'affiliations.value[0]', default='')


def _get_authors_names(record):
    return get_value(record, 'authors.full_name', default=[])