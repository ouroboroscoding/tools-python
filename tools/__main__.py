# coding=utf8
"""Main

Used mainly to test that the module works as expected
"""

# Pip imports
from jobject import JObject

# Import everything
from . import \
	clone, \
	combine, \
	compare, \
	eval, \
	get_client_ip, \
	keys_to_ints, \
	merge, \
	without

_o = {
	'1': 'one',
	'2': 'two',
	'3': 'three'
}
_jo = JObject({
	'one': '1',
	'two': '2',
	'three': '3'
})

print('clone')
o = clone(_o)
jo = clone(_jo)

print('combine')
o = combine(o, {'4': 'four'})
jo = combine(jo, {'four': '4'})

print('compare & without')
print('%s is True' % str(compare(without(o, ['4', '5']), _o)))
print('%s is False' % str(compare(without(o, '4'), jo)))

print('merge')
merge(o, {'5': 'five'})
merge(jo, {'five': '5'})

print('keys_to_ints')
print(keys_to_ints(o))
print(keys_to_ints(jo))

print(without(jo, 'four'))
print(without(jo, ['four', 'five']))
print(without([o, jo], ['4', '5', 'four', 'five']))

print('eval')
try:
	eval(o, [6, 7])
except ValueError as e:
	print(e.args)

get_client_ip({})

# If we got here, everything seems fine
print('I work')