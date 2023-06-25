# Tools by Ouroboros Coding
[![pypi version](https://img.shields.io/pypi/v/Tools-OC.svg)](https://pypi.org/project/Tools-OC) ![MIT License](https://img.shields.io/pypi/l/Tools-OC.svg)

A set of functions for common python problems

## Requires
Tools-OC requires python 3.10 or higher

## Installation
```bash
pip install Tools-OC
```

## Functions

### clone
`clone` is used to make a complete copy of a dictionary from top to bottom. It follows keys that are either dictionaries or lists and clones them as well, but copies anything else as is. Great for copying raw data like JSON, not great for complex structures containing class instances.
```python
>>> from tools import clone
>>> a = {'hello': 'their'}
>>> b = a
>>> a['hello'] = 'there'
>>> b['hello']
'there'
>>> b = clone(a)
>>> a['hello'] = 'fruit loops'
>>> b['hello']
'there'
```

### combine
`combine` is used to generate a new dictionary by cloning the first one passed, then by merging the second into it, and returning it
```python
>>> from tools import combine
>>> a = { 'one': 1 }
>>> b = { 'two': 2 }
>>> c = combine(a, b)
>>> c
{'one': 1, 'two': 2}
>>> d = combine(c, { 'one': 'une' })
>>> d
{'one': 'une', 'two': 2}
```

### compare
`compare` is used to compare any two values. It will compare dicts and lists by traversing them, but will check any other value one to one. Like clone, it is very useful for raw data like JSON, but not great for anything with complex data like class instances unless they take care of overloading \_\_eq\_\_
```python
>>> from tools import compare
>>> compare({'one': 1, 'two': 2}, {'two': 2, 'one': 1})
True
>>> compare([1, 2, 3], [3, 2, 1])
False
>>> compare([{'one': 1}], [{'one': 1}])
True
```

### evaluate
`evaluate` is used to evaluate if a dictionary contains the keys it requires, without a lot of complicated configuration. It's meant for simple dictionaries, but can also check keys of keys
```python
>>> from tools import evaluate
>>> evaluate({'one': 1, 'two': 2}, ['one', 'two', 'three'])
ValueError: three
```

### get_client_ip
Used to get the actual IP address of the client by using the provided dictionary of environment variables
```python
>>> from tools import get_client_ip
>>> from bottle import request
>>> get_client_ip(request.environ)
'195.201.123.59'
```

### keys_to_ints
Traverses a dictionary and converts any keys from strings to integers. Helpful for processing data like JSON that won't allow keys as anything other than strings
```python
>>> from tools import keys_to_ints
>>> keys_to_ints({'1': 'one', '2': 'two'})
{1: 'one', 2: 'two'}
```

### lfindi
Steps through the given list of dictionaries looking for one with a key that matches the value, and returns the index of that dictionary in the list, else -1 for no dictionary found.
```python
>>> from tools import lfindi
>>> l = [
...     {'name': 'Bob', 'job': 'Accountant'},
...     {'name': 'Frank', 'job': 'Salesman'}
... ]
>>> lfindi(l, 'name', 'Frank')
1
>>> lfindi(l, 'name', 'Stan')
-1
```

### lfindd
Works exactly the same as lfindi, but returns the dictionary instead of its index
```python
>>> from tools import lfindd
>>> l = [
...     {'name': 'Bob', 'job': 'Accountant'},
...     {'name': 'Frank', 'job': 'Salesman'}
... ]
>>> lfindd(l, 'name', 'Stan') # Returns None, which does not display
>>> lfindd(l, 'name', 'Frank')
{'name': 'Frank', 'job': 'Salesman'}
```

### merge
Works exactly the same as the `combine` function, but instead of creating a new dict by cloning the first one, that step is skipped and the second dict is simple merged with the first and returned altered
```python
>>> from tools import merge
>>> a = { 'one': 1, 'three': { 'four': 4 } }
>>> b = { 'two': 2, 'three': { 'four': 'quatre' }}
>>> merge(a, b)
{'one': 1, 'three': {'four': 'quatre'}, 'two': 2}
>>> a
{'one': 1, 'three': {'four': 'quatre'}, 'two': 2}
```
`merge` contains an optional third parameter called `return_changes` that will return the differences found while merging the second dict over the first.
```python
>>> from tools import merge
>>> a = { 'one': 1, 'three': { 'four': 4 } }
>>> b = { 'two': 2, 'three': { 'four': 'quatre' }}
>>> merge(a, b, True)
{'two': 2, 'three': {'four': 'quatre'}}
>>> merge(a, {'one': 1, 'three': { 'four': 4 }}, True)
{'three': {'four': 4}}
```

### without
`without` is used to strip out one or more keys from a dictionary, or a list of dictionaries
```python
>>> from tools import without
>>> l = [
...     {'one': 'one', 'two': 'two', 'three': 'three', 'four': 'four'},
...     {'one': 'une', 'two': 'deux', 'three': 'trois', 'four': 'quatre'},
...     {'one': 'uno', 'two': 'dos', 'three': 'tres', 'four': 'cuatro'}
... ]
>>> without(l, ['three', 'four'])
[{'one': 'one', 'two': 'two'}, {'one': 'une', 'two': 'deux'}, {'one': 'uno', 'two': 'dos'}]
>>> without(l[2], 'four')
{'one': 'uno', 'two': 'dos', 'three': 'tres'}
```