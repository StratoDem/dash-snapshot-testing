# dash-snapshot-testing
Use snapshot testing, inspired by Jest snapshot testing, to test [Dash][] components.

## Inspiration
Testing a long HTML component output for a Dash application is difficult.
It typically requires hardcoding data or setting up a dummy database.
Using snapshot tests that JSON serialize the Dash component output provide another
easy testing layer to ensure that code refactors/changes do not change the
output unexpectedly.

To learn more about snapshot testing in general, see a much more elaborate explanation from the [Facebook Jest site](https://facebook.github.io/jest/docs/en/snapshot-testing.html)

## Installation and usage
```bash
$ pip install dash-snapshot-teting
```

```python
import dash_html_components as html

from snapshot_test import DashSnapshotTestCase


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

At its core, this `unittest.TestCase` compares a JSON-serialized Dash component
against a previously stored JSON-serialized Dash component, and checks if the `dict`
objects from `json.loads` are equivalent using `assertEqual`.

[Dash]: https://github.com/plotly/dash
