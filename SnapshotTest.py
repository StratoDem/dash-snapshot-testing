"""
StratoDem Analytics : SnapshotTest
Principal Author(s) : Eric Linden
Secondary Author(s) : 
Description :

Notes : 

March 26, 2018
"""

import json
import os
import plotly.utils
import unittest

from dash.development.base_component import Component


class DashSnapshotUnitTest(unittest.TestCase):
    def assertSnapshotEqual(self, component: Component) -> None:

        # TODO use hash of inputs to create unique pathname?
        # just self.__name__ by itself won't create enough unique names for the various input tests
        filename = self.__get_filename()

        component_json = component.to_plotly_json()

        if os.path.exists(filename):
            expected_dict = json.loads(
                json.dumps(component_json, cls=plotly.utils.PlotlyJSONEncoder))
            self.assertEqual(self.__load_snapshot(), expected_dict)
        else:
            with open(filename, 'w+') as file:
                json.dump(component_json, file, cls=plotly.utils.PlotlyJSONEncoder)

    def __get_filename(self):
        return os.path.join(self.__get_snapshots_dir(), '{}.json'.format(self.__name__))

    def __load_snapshot(self):
        with open(self.__get_filename(), 'r') as f:
            return json.load(f)

    def __get_snapshots_dir(self):
        directory = os.path.join(os.curdir, 'snapshots')

        if not os.path.exists(directory):
            os.mkdir(directory)

        return directory

    # --- All the helpers here


class MyComponentNameTest(DashSnapshotUnitTest):
    def test_func(self) -> None:

        self.assertSnapshotEqual()
