# -*- coding: utf-8 -*-
#
# This file is part of ClaimStore.
# Copyright (C) 2015 CERN.
#
# ClaimStore is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ClaimStore is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClaimStore; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307,
# USA.

"""Claim fixtures."""

import glob
import json
import os

import pytest
from flask import current_app
from webtest import TestApp


@pytest.fixture
def load_all_claims(test_app=None, config_path=None):
    """Fixture that loads all test claims."""
    if test_app is None:
        with current_app.app_context():
            test_app = TestApp(
                current_app,
                extra_environ=dict(REMOTE_ADDR='127.0.0.1')
            )

    if config_path:
        claims_filepath = os.path.join(
            config_path,
            'claims'
        )
    else:
        claims_filepath = os.path.join(
            test_app.app.config['BASE_DIR'],
            'tests',
            'myclaimstore',
            'data',
            'claims'
        )
    for claim_fp in glob.glob("{}/*.json".format(claims_filepath)):
        with open(claim_fp) as f:
            test_app.post_json(
                '/claims',
                json.loads(f.read()))


@pytest.fixture
def dummy_claim():
    """Fixture that creates a dummy claim."""
    return json.loads("""
        {
          "claimant": "dummy_claimant",
          "subject": {
            "type": "CDS_RECORD_ID",
            "value": "2001192"
          },
          "predicate": "is_same_as",
          "certainty": 1.0,
          "object": {
            "type": "CDS_REPORT_NUMBER",
            "value": "CMS-PAS-HIG-14-008"
          },
          "arguments": {
            "human": 0,
            "actor": "CDS_submission"
          },
          "created": "2015-03-25T11:00:00Z"
        }
        """)
