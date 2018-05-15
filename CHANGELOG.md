# CHANGELOG

## 1.2.0 - 2018-05-15
### Changed
- Improves clarity of error messages for large component comparisons
  ##### Old logic:
  raise `AssertionError` with large string difference between JSON objects if the component did not match the snapshot, which led to difficult to read error message like:
  ```
  AssertionError: {'pro[136 chars]en': 'another one'}, 'namespace': 'dash_html_c[77 chars]Div'} != {'pro[136 chars]en': [1, 2, 3]}, 'namespace': 'dash_html_compo[73 chars]Div'}
  ```
  ##### New logic:
  raise `AssertionError` with large string difference between JSON objects if the component does not match the snapshot, **and**
  add new details section about the **first local mismatch** between the component and snapshot:
  ```
  DETAILS:

  <class 'list'> != <class 'str'>
  CONTEXT 1:

  {"children": [1, 2, 3]}

  CONTEXT 2:

  {"children": "another one"}
  ```
  or
  ```
  DETAILS:

  P != Span
  CONTEXT 1:

  {"type": "P", "props": {"children": "another one"}, "namespace": "dash_html_components"}

  CONTEXT 2:

  {"type": "Span", "props": {"children": "another one"}, "namespace": "dash_html_components"}
  ```

## 1.1.0 - 2018-04-11
### Added
- This package now checks for an environment variable (UPDATE_DASH_SNAPSHOTS) and will automatically overwrite snapshots if it is set to TRUE

## 1.0.1 - 2018-03-27
### Added
- MIT License

## 1.0.0 - 2018-03-27
### Added
- Initial publication
