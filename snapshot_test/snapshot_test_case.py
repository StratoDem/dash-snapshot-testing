"""
StratoDem Analytics : SnapshotTest
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

March 26, 2018
"""

import json
import logging
import os
import plotly.utils
import unittest

from dash.development.base_component import Component


__all__ = ['DashSnapshotTestCase']


class DashSnapshotTestCase(unittest.TestCase):
    snapshots_dir = None

    def assertSnapshotEqual(self, component: Component, file_id: str) -> None:
        """
        Tests the supplied component against the specified JSON file snapshot, if it exists.
        If the component and the snapshot match, the test passes. If the specified file is not
        found, it is created and the test passes. This test will only fail if the file already
        exists, and the component-as-JSON does not match the contents of the file. In that event,
        the test will produce a detailed error message showing the differences found. A Dash user
        can set the environment variable "UPDATE_DASH_SNAPSHOTS" to True to replace all existing
        snapshots.

        Parameters
        ----------
        component: Component
            The output of a Dash component that will be rendered to the page
        file_id: str
            A string ID used to distinguish the multiple JSON files that may be used as
            part of a single component's test cases

        Returns
        -------
        None
        """
        assert isinstance(component, Component), 'Component passed in must be Dash Component'
        assert isinstance(file_id, str), 'must pass in a file id to use as unique file ID'

        filename = self.__get_filename(file_id=file_id)

        component_json = component.to_plotly_json()

        if os.path.exists(filename):
            # Check the env variable to see whether snapshots should be replaced
            if os.environ.get('UPDATE_DASH_SNAPSHOTS') == 'TRUE':
                with open(filename, 'w') as file:
                    json.dump(component_json, file, cls=plotly.utils.PlotlyJSONEncoder)
            else:
                # Load a dumped JSON for the passed-in component, to ensure matches standard format
                component_dict = json.loads(json.dumps(component_json,
                                                  cls=plotly.utils.PlotlyJSONEncoder))
                snapshot_dict = self.__load_snapshot(filename=filename)

                try:
                    self.assertEqual(snapshot_dict, component_dict)
                except AssertionError as e:
                    error_msg = self.__generate_error_message(
                        snapshot=snapshot_dict,
                        component=component_dict)
                    # Change the error message here to remove the JSON comparison that isn't useful
                    # Must pass a tuple to e.args otherwise it converts the message into a tuple
                    e.args = error_msg,
                    raise e
        else:
            # Component did not already exist, so we'll write to the file
            with open(filename, 'w') as file:
                json.dump(component_json, file, cls=plotly.utils.PlotlyJSONEncoder)

    def __get_filename(self, file_id: str) -> str:
        """
        Builds and returns the path for the specific JSON file used in this test.

        Parameters
        ----------
        file_id: str
            A string ID used to distinguish the multiple JSON files that may be used as
            part of a single component's test cases

        Returns
        -------
        A string containing the path to the file.
        """
        assert isinstance(file_id, str)

        return os.path.join(
            self.__get_snapshots_dir(),
            '{}-{}.json'.format(self.__class__.__name__, file_id))

    @staticmethod
    def __load_snapshot(filename: str) -> dict:
        """
        Opens the JSON file at the specified location and returns its contents in dict form.

        Parameters
        ----------
        filename: str
            The path to the JSON file

        Returns
        -------
        A dict of the JSON file contents.
        """
        assert isinstance(filename, str)

        with open(filename, 'r') as f:
            return json.load(f)

    @classmethod
    def __get_snapshots_dir(cls) -> str:
        """
        Checks for the existence of the snapshots directory, and creates it if it is not found.
        It then returns the directory path.

        Returns
        -------
        A string containing the path of the snapshots directory.
        """
        if cls.snapshots_dir is None:
            directory = os.path.join(os.curdir, '__snapshots__')

            if not os.path.exists(directory):
                os.mkdir(directory)

            return directory
        else:
            if not os.path.exists(cls.snapshots_dir):
                os.mkdir(cls.snapshots_dir)

            return cls.snapshots_dir

    @classmethod
    def __generate_error_message(cls, snapshot: dict, component: dict):
        """

        Parameters
        ----------
        snapshot
        component

        Returns
        -------

        """
        assert isinstance(snapshot, dict)
        assert isinstance(component, dict)

        error_message = 'The following differences were found:\n'
        cmpnt_strucuture = 'Component skeleton:\n'
        element_id = 0
        indentation = 0

        def check_contents(snapshot, component):
            nonlocal element_id, error_message, cmpnt_strucuture, indentation
            if isinstance(snapshot, dict) and isinstance(component, dict):
                indentation += 2
                pairs = snapshot.items() if len(snapshot) > len(component) else component.items()

                for key, val in snapshot.items():
                    element_id += 1
                    # TODO should the entire val be shown here?
                    # I tried using a conditional to avoid showing certain ones (children and props)
                    # but couldn't get it right for some reason
                    cmpnt_strucuture += '{id} - {indent}{key} - {val}\n'.format(
                        id=element_id,
                        indent=' ' * indentation,
                        key=key,
                        val=val)
                    if key in component:
                        if isinstance(val, dict) or isinstance(val, list):
                            check_contents(snapshot=val, component=component[key])
                        else:
                            if val != component[key]:
                                error_message += cls.__make_error_entry(
                                    element_id=element_id,
                                    snapshot=val,
                                    component=component[key])
                indentation -= 2
            elif isinstance(snapshot, list) and isinstance(component, list):
                if len(snapshot) != len(component):
                    error_message += cls.__make_error_entry(
                        element_id=element_id,
                        snapshot=snapshot,
                        component=component)
                else:
                    for i in range(len(snapshot)):
                        check_contents(snapshot=snapshot[i], component=component[i])
            else:
                if snapshot != component:
                    error_message += cls.__make_error_entry(
                        element_id=element_id,
                        snapshot=snapshot,
                        component=component)

        check_contents(snapshot=snapshot, component=component)

        logging.error(cmpnt_strucuture)
        return error_message

    @staticmethod
    def __make_error_entry(element_id, snapshot, component):
        return 'Element id: {id}\n' \
               '  Snapshot: {snapshot_value}\n' \
               '  Component: {component_value}\n'.format(
                  id=element_id,
                  snapshot_value=snapshot,
                  component_value=component)
