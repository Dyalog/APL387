import fontforge
import os
import sys

EXTENSIONS = [
	'ttf',
	'otf',
	'woff',
	'woff2',
	'svg',
]

path = sys.argv[1]

apl387 = fontforge.open(f'{path}/APL387.ufo2')

print(apl387.version)

apl387.version = os.getenv('COMMIT') or 'unknown'

print(apl387.version)

try:
	os.mkdir(f'{path}/output')
except:
	pass

with open(f'{path}/output/chars.html', 'w') as chars:
	chars.write('''
<html lang="en">
  <head>
    <meta charset="utf-8" /> 
    <title>Characters - APL385 vs new APL387</title>
    <style>
@font-face {font-family: 'APL385';src: url('APL385.ttf');}
@font-face {font-family: 'APL387';src: url('APL387.ttf');}
td{text-align:center;font-size:200}
td:first-child{font-family:APL385}
td:last-child{font-family:APL387}
span{white-space:pre}
</style>
</head>
<body onload="w=document.querySelector`span`.offsetWidth;document.querySelectorAll`span`.forEach(e=>e.style.opacity=0.2**(e.offsetWidth!=w))">
<table>
<tr><th>APL385 Unicode</th><th>new APL387 Unicode</th></tr>
	''')
	for gl in sorted((gl for gl in apl387.glyphs() if gl.unicode != -1), key=lambda gl: gl.unicode):
		chars.write(f'<tr><td><span>&#{gl.unicode};</span></td><td><span>&#{gl.unicode};</span></td></tr>\n')
	chars.write('''
</table>
</body>
</html>
	''')

for ext in EXTENSIONS:
	apl387.generate(f'{path}/output/APL387.{ext}')	
