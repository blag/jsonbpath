import jsonpath_rw
from mock import Mock

from jsonbpath import generate_jsonb_query


# Query mock
query = Mock()
query.filter = Mock()

# Column mock
column = Mock()
column.has_key = Mock()
column.contains = Mock()

# Data
data = {
    'extra': {
        'expires': {
            'integer': 4,
        },
        'array': [4, 3, 2, 1],
    },
}

generate_jsonb_query(query, column, 'extra.expires')

column.has_key.assert_called_with(('extra', 'expires',))

assert query.filter.call_count > 0


# RESET
column.has_key.reset_mock()
query.filter.reset_mock()

assert column.has_key.call_count == 0
assert query.filter.call_count == 0


generate_jsonb_query(query, column, 'extra.expires.integer', 4)

column.contains.assert_called_with({'extra': {'expires': {'integer': 4}}})
assert query.filter.call_count > 0


# RESET
column.has_key.reset_mock()
query.filter.reset_mock()

assert column.has_key.call_count == 0
assert query.filter.call_count == 0


# Pass in a compiled jsonpath to begin with
jsonpath = jsonpath_rw.parse('extra.expires')
generate_jsonb_query(query, column, jsonpath)

column.has_key.assert_called_with(('extra', 'expires',))

assert query.filter.call_count > 0


# RESET
column.has_key.reset_mock()
query.filter.reset_mock()

assert column.has_key.call_count == 0
assert query.filter.call_count == 0


# Filter using slices
assertion_raised = False
try:
    generate_jsonb_query(query, column, 'extra.array[*]', 4)
except NotImplementedError as e:
    assert e.args[0] == "Filtering using slices is not supported."
