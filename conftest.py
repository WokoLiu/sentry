from __future__ import absolute_import

import os
import sys
from hashlib import md5

import pytest

pytest_plugins = [
    'sentry.utils.pytest'
]

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
NUM_TEST_GROUPS = 2


def pytest_configure(config):
    import warnings
    # XXX(dcramer): Riak throws a UserWarning re:OpenSSL which isnt important
    # to tests
    # XXX(dramer): Kombu throws a warning due to transaction.commit_manually
    # being used
    warnings.filterwarnings('error', '', Warning, r'^(?!(|kombu|raven|riak|sentry))')


def pytest_collection_modifyitems(items):
    for item in items:
        group_num = int(md5(item.location[0]).hexdigest(),
                        16) % os.environ.get('TOTAL_TEST_GROUPS', 1)
        item.add_marker(getattr(pytest.mark, 'group_%s' % group_num))
