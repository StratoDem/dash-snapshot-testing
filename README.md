# dash-snapshot-testing
Use snapshot testing to test Dash components


## Example
```python
 class MyComponentNameTest(DashSnapshotUnitTest):
     def test_func(self) -> None:

         self.assertSnapshotEqual()
```