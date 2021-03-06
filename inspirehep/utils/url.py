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
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Helpers for handling with http requests and URL handling."""

from __future__ import absolute_import, division, print_function

from flask import current_app

from inspirehep import __version__


def make_user_agent_string(component=""):
    """Return a nice and uniform user-agent string to be used by INSPIRE."""
    ret = "InspireHEP-{0} (+{1};)".format(
        __version__,
        current_app.config.get('SERVER_NAME', ''),
    )
    if component:
        ret += " [{}]".format(component)
    return ret
