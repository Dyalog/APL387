import fontforge
import os
import sys

EXTENSIONS = [
	'ttf',
	'otf',
	'woff',
	'woff2',
	'svg'
]

path = sys.argv[1]

apl387 = fontforge.open(f'{path}/APL387.ufo2')

os.mkdir(f'{path}/output')

for ext in EXTENSIONS:
	apl387.generate(f'{path}/output/APL387.{ext}')
