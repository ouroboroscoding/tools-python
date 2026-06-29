# tools_oc releases

## 1.2.7
- Added the `keep` method. Works as an opposite of `without` by returning a new
copy of a dict with only the keys requested.

## 1.2.6
- Marked `clone` as deprecated, users should use Python's `copy.deepcopy` method
instead