"""
StratoDem Analytics : __test_snapshot_test_case
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

March 27, 2018
"""


import dash_html_components as html

from snapshot_test import DashSnapshotTestCase


class MyUnitTestCase(DashSnapshotTestCase):
    def test_component(self):
        my_component = html.Div([html.P('wow!'), html.Span('this works')], id='test-id')

        self.assertSnapshotEqual(my_component, 'my-test-unique-id')


class MyOtherUnitTestCase(DashSnapshotTestCase):
    snapshots_dir = '__snapshots_2__'

    def test_component(self):
        my_component = html.Div([html.P('wow'), html.Span('another one')], id='test-id')

        self.assertSnapshotEqual(my_component, 'my-test-unique-id')
