#!/usr/bin/env python
#
# Copyright 2011-2015 Jeff Bush
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Create an assembly test that verifies all major instruction forms and
# single cycle integer operations
#

import random
import sys

forms = [
	('s', 's', 's', ''),
	('v', 'v', 's', ''),
	('v', 'v', 's', '_mask'),
	('v', 'v', 'v', ''),
	('v', 'v', 'v', '_mask'),
	('s', 's', 'i', ''),
	('v', 'v', 'i', ''),
	('v', 'v', 'i', '_mask'),
	('v', 's', 'i', ''),
	('v', 's', 'i', '_mask'),
]

binops = [
	'or',
	'and',
	'xor',
	'add_i',
	'sub_i',
	'mull_i',
	'mulh_u',
	'mulh_i',
	'ashr',
	'shr',
	'shl',
]

unops = [
	'clz',
	'ctz',
	'move'
]

print('# This file auto-generated by ' + sys.argv[0] + '''. Do not edit.
			.include "macros.inc"

			.globl _start
			.align 64
value1:		.long 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
value2:		.long 0xaaaaaaaa, 0xbbbbbbbb, 0xcccccccc, 0xdddddddd, 0xeeeeeeee, 0xffffffff
			.long 0x11111111, 0x22222222, 0x33333333, 0x44444444, 0x55555555, 0x66666666
			.long 0x77777777, 0x88888888, 0x99999999
mask:		.long 0x5a5a

_start:		move v0, 0
			load_v v2, value2
			load_v v3, value1
			move s2, 0x456
			move s3, 0x123
			load_32 s10, mask
''')

dest = 1
rega = 2
regb = 3
for td, ta, tb, suffix in forms:
	for mnemonic in binops:
		opstr = '\t\t' + mnemonic + suffix + ' ' + td + str(dest) + ', '
		if suffix != '':
			opstr += 's10, '  # Mask register

		opstr += ta + str(rega) + ', '
		if tb == 'i':
			opstr += str(random.randint(0, 0x1ff))
		else:
		 	opstr += tb + str(regb)
		print(opstr)

		# Cycle registers
		tmp = regb
		regb = rega
		rega = dest
		dest = tmp

for td, ta, tb, suffix in forms:
	if tb == 'i':
		continue

	for mnemonic in unops:
		opstr = '\t\t' + mnemonic + suffix + ' ' + td + str(dest) + ', '
		if suffix != '':
			opstr += 's10, '

		opstr += ta + str(rega)
		print(opstr)

		# Cycle registers
		tmp = rega
		rega = dest
		dest = tmp

print('\t\tHALT_CURRENT_THREAD\n')
