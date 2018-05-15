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
from typing import Any

from dash.development.base_component import Component


__all__ = ['DashSnapshotTestCase']


class DashSnapshotMismatch(Exception):
    pass


class DashSnapshotTestCase(unittest.TestCase):
    snapshots_dir = None

    def assertSnapshotEqual(self, component: Component, file_id: str) -> None:
        """
        Tests the supplied component against the specified JSON file snapshot, if it exists.
        If the component and the snapshot match, the test passes. If the specified file is not
        found, it is created and the test passes. This test will only fail if the file already
        exists, and the component-as-JSON does not match the contents of the file. A Dash user can
        set the environment variable "UPDATE_DASH_SNAPSHOTS" to True to replace all existing
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
                expected_dict = json.loads(
                    json.dumps(component_json, cls=plotly.utils.PlotlyJSONEncoder))
                existing_snapshot = self.__load_snapshot(filename=filename)
                try:
                    self.__check_object_equality(
                        expected_dict,
                        existing_snapshot,
                        context1=expected_dict,
                        context2=existing_snapshot)
                except DashSnapshotMismatch as e:
                    self.assertEqual(
                        existing_snapshot,
                        expected_dict,
                        '\n\nDETAILS:\n\n{}'.format(e))
                self.assertEqual(
                    existing_snapshot,
                    expected_dict)
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
    def __check_object_equality(cls, obj1: Any, obj2: Any, context1: Any, context2: Any) -> None:
        if type(obj1) != type(obj2):
            raise DashSnapshotMismatch(
                '{} != {} {}'.format(
                    type(obj1),
                    type(obj2),
                    cls.__create_error_context(context1, context2)))
        elif isinstance(obj1, (list, tuple)):
            if len(obj1) != len(obj2):
                raise DashSnapshotMismatch(
                    'Length of object 1 ({}) does not match object 2 ({}) {}'.format(
                        len(obj1),
                        len(obj2),
                        cls.__create_error_context(obj1, obj2)))
            else:
                for obj1_element, obj2_element in zip(obj1, obj2):
                    cls.__check_object_equality(
                        obj1=obj1_element,
                        obj2=obj2_element,
                        context1=obj1,
                        context2=obj2)
        elif isinstance(obj1, dict):
            if set(obj1.keys()) != set(obj2.keys()):
                raise DashSnapshotMismatch(
                    'Keys do not match ({} vs {}) {}'.format(
                        obj1.keys(),
                        obj2.keys(),
                        cls.__create_error_context(context1, context2)))
            else:
                for k1 in obj1.keys():
                    cls.__check_object_equality(
                        obj1=obj1[k1],
                        obj2=obj2[k1],
                        context1=obj1,
                        context2=obj2)
        elif isinstance(obj1, (str, int, float)) or obj1 is None:
            if obj1 != obj2:
                raise DashSnapshotMismatch(
                    '{} != {} {}'.format(
                        obj1,
                        obj2,
                        cls.__create_error_context(context1, context2)))
        else:
            raise TypeError('DashSnapshotTesting does not support type {}'.format(type(obj1)))

    @staticmethod
    def __create_error_context(context1: Any, context2: Any) -> str:
        return '\nCONTEXT 1:\n\n{}\n\nCONTEXT 2: \n\n{}'.format(
                    json.dumps(context1),
                    json.dumps(context2))
