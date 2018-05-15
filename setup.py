"""
StratoDem Analytics : setup
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

March 27, 2018
"""

from setuptools import setup

setup(
    name='dash-snapshot-testing',
    version='1.2.2',
    author='Michael Clawar, Eric Linden',
    author_email='tech@stratodem.com',
    packages=['snapshot_test'],
    license='MIT',
    description='Dash snapshot testing package',
    url='https://github.com/StratoDem/dash-snapshot-testing',
    keywords='dash snapshot plotly testing unittest',
    python_requires='>=3',
    install_requires=[
        'dash>=0.19.0',
        'plotly>=2.2.3',
    ],
    long_description="""
# dash-snapshot-testing
Use snapshot testing, inspired by Jest snapshot testing, to test [Dash][] components.

See the project [README](https://github.com/StratoDem/dash-snapshot-testing/blob/master/README.md) for more detailed information.

## Inspiration
Testing a long HTML component output for a Dash application is difficult.
It typically requires hardcoding data or setting up a dummy database.
Using snapshot tests that JSON serialize the Dash component output provide another
easy testing layer to ensure that code refactors/changes do not change the
output unexpectedly.

To learn more about snapshot testing in general, see a much more elaborate explanation from the [Facebook Jest site](https://facebook.github.io/jest/docs/en/snapshot-testing.html)

## Installation and usage
```bash
$ pip install dash-snapshot-testing
```

```python
import dash_html_components as html

from dash_snapshot_testing.snapshot_test import DashSnapshotTestCase


class MyUnitTestCase(DashSnapshotTestCase):
    def test_component(self):
        my_component = html.Div([html.P('wow'), html.Span('this works')], id='test-id')

        self.assertSnapshotEqual(my_component, 'my-test-unique-id')
```

This outputs/checks this JSON at `__snapshots__/MyUnitTestCase-my-test-unique-id.json`:
```json
{
  "type": "Div",
  "props": {
    "id": "test-id",
    "children": [
      {
        "type": "P",
        "props": {"children": "wow"},
        "namespace": "dash_html_components"
      },
      {
        "type": "Span",
        "props": {"children": "this works"},
        "namespace": "dash_html_components"
      }
    ]
  },
  "namespace": "dash_html_components"
}
```

### Setting a custom `snapshots_dir` for the class
```python
class MyOtherUnitTestCase(DashSnapshotTestCase):
    snapshots_dir = '__snapshots_2__'

    def test_component(self):
        my_component = html.Div([html.P('wow'), html.Span('another one')], id='test-id')

        self.assertSnapshotEqual(my_component, 'my-test-unique-id')
```

This outputs/checks this JSON at `__snapshots_2__/MyOtherUnitTestCase-my-test-unique-id.json`:
```json
{
  "type": "Div",
  "props": {
    "id": "test-id",
    "children": [
      {
        "type": "P",
        "props": {"children": "wow"},
        "namespace": "dash_html_components"
      },
      {
        "type": "Span",
        "props": {"children": "another one"},
        "namespace": "dash_html_components"
      }
    ]
  },
  "namespace": "dash_html_components"
}
```

### Overwriting snapshots
To overwrite pre-existing snapshots, [like in Jest](https://facebook.github.io/jest/docs/en/snapshot-testing.html#updating-snapshots), set an environment variable as `UPDATE_DASH_SNAPSHOTS=TRUE`:
```bash
# This will run and make new snapshots
> UPDATE_DASH_SNAPSHOTS=TRUE python -m unittest my_test_module
# This will run against the previous snapshots
> python -m unittest my_test_module
```

### How this works
At its core, this `unittest.TestCase` compares a JSON-serialized Dash component
against a previously stored JSON-serialized Dash component, and checks if the `dict`
objects from `json.loads` are equivalent using `assertEqual`.

[Dash]: https://github.com/plotly/dash    
""")
