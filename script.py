import fontforge
import os
import sys
from itertools import chain, combinations
import csv
import tomllib

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

EXTENSIONS = [
  'ttf',
  'otf',
  'woff',
  'woff2',
  'svg',
]

path = sys.argv[1]
commit = sys.argv[2]

apl387 = fontforge.open(f'{path}/APL387.ufo2')

apl387.version = commit

braille_dots = [apl387.createMappedChar(f'part_braille_dot_{i+1}') for i in range(8)]

for braille_index in range(0x100):
	glyph = apl387.createChar(0x2800 + braille_index)
	apl387.selection.select('space')
	apl387.copy()
	apl387.selection.select(glyph)
	apl387.paste()
	bits = [ch == '1' for ch in bin(braille_index)[2:].rjust(8, '0')][::-1]
	if braille_index in [0x1b, 0xc0]:
		print(bits)
	for bit_idx, bit in enumerate(bits):
		if bit:
			apl387.selection.select(braille_dots[bit_idx])
			apl387.copy()
			apl387.selection.select(glyph)
			apl387.pasteInto()

try:
  os.mkdir(f'{path}/output')
except:
  pass

features = [apl387.getLookupInfo(lookup)[2][0][0] for lookup in apl387.gsub_lookups]

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

def compare_page(font, old, new, propo = False, name = 'compare'):
  with open(f'{path}/output/{name}.html', 'w', encoding='utf-8') as compare:
    compare.write(f'''
  <html lang="en">
    <head>
      <meta charset="utf-8" /> 
      <title>{new} Comparison</title>
      <style>
@font-face {'{'}font-family: '{new}';src: url('{new}.ttf');{'}'}
@font-face {'{'}font-family: '{old}';src: url('{old}.ttf');{'}'}
#{old}{'{'}font-family:{old}!important{'}'}
#{new}{'{'}font-family:{new}!important{'}'}
''' + '''
* {
  font-weight: unset;
  font-feature-settings: inherit;
}

body {
  font-size: 200%;
  line-height: 1.2;
  margin:0;
}
blockquote {
  -webkit-hyphens: auto;
  -ms-hyphens: auto;
  hyphens: auto;
  font-size: 125%;
  word-break: break-all;
}
pre{font-family:inherit}
textarea {
  width: 100%;
  resize: vertical;
  min-height: 4em;
  font-size: inherit;
  font-family: inherit;
  font-size:inherit;
}
table{font-size:inherit}
section{width:49vw;overflow:hidden;display:inline-block;top:0;vertical-align:top}
</style>
    </head>
    <body>
    ''')
    for feature in features:
      compare.write(f'<input id="{feature}" type="checkbox" name="{feature}" value="{feature}"><label for="{feature}">{feature}</label>')
    compare.write('<br><a href="./chars">compare characters individually</a>')
    same = '''
<textarea id="ta385" placeholder="Try it yourself ― type here!" spellcheck="false" oninput"ta387.value=this.value"></textarea>
<p>Supports every special character used by any APL implementation:</p>
<table>
<tbody><tr><th>Class</th>
<th>Glyphs
</th></tr>
<tr><td>alphas</td><td>⍺⍶</td></tr>
<tr><td>arrows-down</td><td>↓⍗⍖</td></tr>
<tr><td>arrows-left</td><td>←⍇⍅</td></tr>
<tr><td>arrows-right</td><td>→⍈⍆➥</td></tr>
<tr><td>arrows-up</td><td>↑⍐⍏</td></tr>
<tr><td>asterisks</td><td>*⍣⍟⋆</td></tr>
<tr><td>brackets</td><td>[]⌈⌊⌷</td></tr>
<tr><td>circles</td><td>○⍥⍟⌽⍉⊖⍜⊙⌾∅</td></tr>
<tr><td>colons</td><td>:⍠÷⌹</td></tr>
<tr><td>commas</td><td>,⍪;⍮</td></tr>
<tr><td>dashes</td><td>-+±÷⌹⌿⍀⍪⍏⍖⊢⊣</td></tr>
<tr><td>dels</td><td>∇⍒⍫⍢</td></tr>
<tr><td>deltas</td><td>∆⍙⍋⍍</td></tr>
<tr><td>diamonds</td><td>⋄⌺⍚</td></tr>
<tr><td>diereses</td><td>¨⍨⍥⍤⍣⍢⍡⍩ᑈᐵ</td></tr>
<tr><td>dots</td><td>.:,;?!‼⍰</td></tr>
<tr><td>epsilons</td><td>∊⍷</td></tr>
<tr><td>equals</td><td>=≠⌸⍯</td></tr>
<tr><td>iotas</td><td>⍳⍸</td></tr>
<tr><td>jots</td><td>∘⍤⍛⍝⍎⍕¤⌾⟃⟄</td></tr>
<tr><td>letters</td><td>⍺⍶∆⍙∂∊⍷⍳⍸λπ⍴ϼχ∫</td></tr>
<tr><td>omegas</td><td>⍵⍹</td></tr>
<tr><td>quads</td><td>⎕⌸⌹⌺⌻⌼⍁⍂⍃⍄⍇⍈⍌⍍⍐⍓⍯⍰</td></tr>
<tr><td>shoes-down</td><td>∪⍦</td></tr>
<tr><td>shoes-left</td><td>⊂⊆⍧⟃</td></tr>
<tr><td>shoes-right</td><td>⊃⊇⟄</td></tr>
<tr><td>shoes-up</td><td>∩⋔</td></tr>
<tr><td>slashes</td><td>/⌿⍁%</td></tr>
<tr><td>slashes-back</td><td>\⍀⍉⍂</td></tr>
<tr><td>stiles</td><td>|⌽⍒⍋∥⍭¦⍦⍧$</td></tr>
<tr><td>tacks-down</td><td>⌶⊤⍕⍑⍡</td></tr>
<tr><td>tacks-up</td><td>⌶⊥⍎⍊</td></tr>
<tr><td>tildes</td><td>~⍬⍭⍱⍲</td></tr>
<tr><td>underscores</td><td>_⍙⍷⍛⍸⊆⊇⍊⍜⍶⍹⍮⍚⍘</td></tr>
<tr><td>wedges-down</td><td>∨⍱⍌</td></tr>
<tr><td>wedges-left</td><td>&lt;≤⍃ᑈ</td></tr>
<tr><td>wedges-right</td><td>&gt;≥⍄⍩ᐵ</td></tr>
<tr><td>wedges-up</td><td>∧⍲⍓</td></tr></tbody></table>
<p>Vertical alignment: +-×÷*⊂∘○~←⌶⊥⊢<=</p>
    <p>And many additional mathematical, typographical, pictogram symbols:</p>
    <blockquote>
      ¦‖¬°∓µ·∵¼½¾↔↕∉≉≣⊖⊕⊖⊗⊘⊝⊛⊻⊼⊽⋔⌈⌉⌊⌋<br>
      `´¡¿‼‽¢£¤¥ © ® ºª«»‘’‚‛“”„‟§¶<br>
      ♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♀♂
    </blockquote>''' + ('''
    <p>Single and double line drawing characters, and blocks and shades:</p>
    <blockquote style="line-height: 1.15;">┌─┬┐ ╔═╦╗ ▁▂▃▄▅▆▇█<br>
              │ ││ ║ ║║ █▉▊▋▌▍▎▏<br>
              ├─┼┤ ╠═╬╣ ▌▀▄▐<br>
              └─┴┘ ╚═╩╝ ░▒▓</blockquote>''' if not propo else '') + '''
    <p>Includes both uppercase and lowercase underscored alphabets, plus superscript and subscript digits:</p>
    <blockquote>
      ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ<br>
      ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ<br>
      ⁰¹²³⁴⁵⁶⁷⁸⁹ ₀₁₂₃₄₅₆₇₈₉</blockquote>
    <p>Extensive set of accented Latin letters:</p>
    <blockquote style="word-break: break-all;">ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĆćĈĉĊċĖėĠġĢģĤĥĨĩİıĴĵĶķĹĺĻļŃńŅņŔŕŖŗŚśŜŝŨũŴŵŶŷŸŹźŻżƒǴǵǸǹǼǽǾǿȨȩȮȯ</blockquote>
    <p>Full support for Greek:</p>
    <blockquote>Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϕϖϜϝϲϳϴϵ϶ϷϸϹϼϽϾϿ</blockquote>
    <p>And Cyrillic:</p>
    <blockquote>ЀЁЂЃЄЅІЇЈЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяѐёѓєѕіїјў</blockquote>
    <p>Sample APL code:</p>
    <blockquote style="line-height: 1;"><pre style="font-family: inherit;">''' + ('''
w←⊃(⊃0⍴⍵){                           ⍝┌┌─2─┐       monadic; use ↓
    (e a)←|⍺                         ⍝├ 0 0 1 1 1  dyadic; use /
    T←⌽⍣(0&gt;⊃⌽⍺)                      ⍝└──→⍺⍺←─────┐
    Pad←⍵⍵⍉(T⊣)⍪⍵⍪(T⊢)               ⍝ ┌⍺┐  ⌺     │
    need←(1+e),1↓⍴⍵                  ⍝ ┌─────⍵⍵──┐┘
    a=0:(1↓need⍴0↑⍵)Pad(1↓need⍴0↑⊢⍵) ⍝  0 0│1 2 3 4 5│0 0  Zero
    a=1:(1↓need⍴1↑⍵)Pad(1↓need⍴1↑⊖⍵) ⍝  1 1│1 2 3 4 5│5 5  Replicate
    a=2:(⊖¯1↓need⍴⊢⍵)Pad(¯1↓need⍴⊖⍵) ⍝  2 1│1 2 3 4 5│5 4  Reverse
    a=3:(⊖⊢1↓need⍴⊢⍵)Pad(⊢1↓need⍴⊖⍵) ⍝  3 2│1 2 3 4 5│4 3  Mirror
    a=4:(⊖¯1↓need⍴⊖⍵)Pad(¯1↓need⍴⊢⍵) ⍝  4 5│1 2 3 4 5│1 2  Wrap
}(¯1⌽⍳≢⍴⍵)/(⌽extra,¨⍺⊣0),⊂⍵          ⍝     └────⍵────┘''' if not propo else '''
w←⊃(⊃0⍴⍵){
    (e a)←|⍺
    T←⌽⍣(0&gt;⊃⌽⍺)
    Pad←⍵⍵⍉(T⊣)⍪⍵⍪(T⊢)
    need←(1+e),1↓⍴⍵
    a=0:(1↓need⍴0↑⍵)Pad(1↓need⍴0↑⊢⍵)
    a=1:(1↓need⍴1↑⍵)Pad(1↓need⍴1↑⊖⍵)
    a=2:(⊖¯1↓need⍴⊢⍵)Pad(¯1↓need⍴⊖⍵)
    a=3:(⊖⊢1↓need⍴⊢⍵)Pad(⊢1↓need⍴⊖⍵)
    a=4:(⊖¯1↓need⍴⊖⍵)Pad(¯1↓need⍴⊢⍵)
}(¯1⌽⍳≢⍴⍵)/(⌽extra,¨⍺⊣0),⊂⍵''') + '''</pre></blockquote>
      <p>Sample text:</p>
      <blockquote>APL (named after the book A Programming Language) is a programming language developed in the 1960s by Kenneth E. Iverson. Its central datatype is the multidimensional array. It uses a large range of special graphic symbols to represent most functions and operators, leading to very concise code. It has been an important influence on the development of concept modeling, spreadsheets, functional programming, and computer math packages. It has also inspired several other programming languages.</blockquote>
  <p>All supported characters:</p>
  <pre>
    '''
    for idx, gl in enumerate(sorted((gl for gl in font.glyphs() if gl.unicode != -1), key=lambda gl: gl.unicode)):
      if idx != 0 and idx % 16 == 0: same += '\n'
      same += f'&#{gl.unicode};'
    same += '</pre>'
    compare.write(f'''
  <div>
  <section id='{old}'><h2>{old} Unicode</h2>
    {same}
  </section>
  <section id='{new}'><h2>New {new} Unicode</h2>
    {same}
  </section>
  </div>
    <script src="features.js"></script>
    </body>
  </html>
    ''')

def index_page(old, new, propo = False, name = 'index', compare_name = 'compare'):
  with open(f'{path}/output/{name}.html', 'w', encoding='utf-8') as index:
    index.write(f'''
<html lang="en">
  <head>
    <meta charset="utf-8" /> 
    <title>{new} - A New {old}</title>
    <link rel="shortcut icon" href="favicon.ico"/>
    <link rel="stylesheet" href="index.css">
  </head>
  <body>
    <div class="c">
      <input id="{new}" class="x" type="radio" name="f" value="{new}" checked=""><label class="x" for="APL387">{new}.ttf</label>
      <input id="{old}" class="x" type="radio" name="f" value="{old}"           ><label class="x" for="APL387">{old}.ttf</label>
      <br>
  ''')
    for feature in features:
      index.write(f'<input id="{feature}" type="checkbox" name="{feature}" value="{feature}"><label for="{feature}">{feature}</label>')
    index.write(f'''
    </div>
    <h1>{new} Unicode<sup> <a href="{new}.ttf">download</a> <a href="" id="wb">download with baked features</a></sup> <span><sup><a href="./{compare_name}">side by side with {old}</a></sup> <sup><a href="https://github.com/dyalog/APL387">source</a></sup></span></h1>
    <p>A redrawn and extended version of Adrian Smith's classic <a href="https://apl385.com/fonts/index.htm">{old}</a> font with clean rounded look.</p>
    <p><a href=".">APL387 (monospace)</a> <a href="./335">APL335 (proportional)</a></p>
    <blockquote>
      <textarea autofocus placeholder="Try it yourself ― type here!" spellcheck="false"></textarea>
    </blockquote>
    <p>Supports every special character used by any APL implementation:</p>
<table>
<tbody><tr><th>Class</th>
<th>Glyphs
</th></tr>
<tr><td>alphas</td><td>⍺⍶</td></tr>
<tr><td>arrows-down</td><td>↓⍗⍖</td></tr>
<tr><td>arrows-left</td><td>←⍇⍅</td></tr>
<tr><td>arrows-right</td><td>→⍈⍆➥</td></tr>
<tr><td>arrows-up</td><td>↑⍐⍏</td></tr>
<tr><td>asterisks</td><td>*⍣⍟⋆</td></tr>
<tr><td>brackets</td><td>[]⌈⌊⌷</td></tr>
<tr><td>circles</td><td>○⍥⍟⌽⍉⊖⍜⊙⌾∅</td></tr>
<tr><td>colons</td><td>:⍠÷⌹</td></tr>
<tr><td>commas</td><td>,⍪;⍮</td></tr>
<tr><td>dashes</td><td>-+±÷⌹⌿⍀⍪⍏⍖⊢⊣</td></tr>
<tr><td>dels</td><td>∇⍒⍫⍢</td></tr>
<tr><td>deltas</td><td>∆⍙⍋⍍</td></tr>
<tr><td>diamonds</td><td>⋄⌺⍚</td></tr>
<tr><td>diereses</td><td>¨⍨⍥⍤⍣⍢⍡⍩</td></tr>
<tr><td>dots</td><td>.:,;?!⍰</td></tr>
<tr><td>epsilons</td><td>∊⍷</td></tr>
<tr><td>equals</td><td>=≠⌸⍯</td></tr>
<tr><td>iotas</td><td>⍳⍸</td></tr>
<tr><td>jots</td><td>∘⍤⍛⍝⍎⍕¤⌾⟃⟄</td></tr>
<tr><td>letters</td><td>⍺⍶∆⍙∂∊⍷⍳⍸λπ⍴ϼχ∫</td></tr>
<tr><td>omegas</td><td>⍵⍹</td></tr>
<tr><td>quads</td><td>⎕⌸⌹⌺⌻⌼⍁⍂⍃⍄⍇⍈⍌⍍⍐⍓⍯⍰</td></tr>
<tr><td>shoes-down</td><td>∪⍦</td></tr>
<tr><td>shoes-left</td><td>⊂⊆⍧⟃</td></tr>
<tr><td>shoes-right</td><td>⊃⊇⟄</td></tr>
<tr><td>shoes-up</td><td>∩⋔⍝</td></tr>
<tr><td>slashes</td><td>/⌿⍁%</td></tr>
<tr><td>slashes-back</td><td>\⍀⍉⍂</td></tr>
<tr><td>stiles</td><td>|⌽⍒⍋∥⍭⍦⍧$</td></tr>
<tr><td>tacks-down</td><td>⌶⊤⍕⍑⍡</td></tr>
<tr><td>tacks-up</td><td>⌶⊥⍎⍊</td></tr>
<tr><td>tildes</td><td>~⍬⍭⍱⍲</td></tr>
<tr><td>underscores</td><td>_⍙⍷⍛⍸⊆⊇⍊⍜⍶⍹⍮⍚⍘</td></tr>
<tr><td>wedges-down</td><td>∨⍱⍌</td></tr>
<tr><td>wedges-left</td><td>&lt;≤⍃ᑈ</td></tr>
<tr><td>wedges-right</td><td>&gt;≥⍄⍩ᐵ</td></tr>
<tr><td>wedges-up</td><td>∧⍲⍓</td></tr></tbody></table>
    <p>And many additional mathematical, typographical, pictogram symbols:</p>
    <blockquote>
      ¦‖¬°∓µ·∵¼½¾↔↕∉≉≣⊖⊕⊖⊗⊘⊝⊛⊻⊼⊽⋔⌈⌉⌊⌋<br>
      `´¡¿‼‽¢£¤¥ © ® ºª«»‘’‚‛“”„‟§¶<br>
      ♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♀♂
    </blockquote>''' + ('''
    <p>Single and double line drawing characters, and blocks and shades:</p>
    <blockquote style="line-height: 1.15;">┌─┬┐ ╔═╦╗ ▁▂▃▄▅▆▇█<br>
               │ ││ ║ ║║ █▉▊▋▌▍▎▏<br>
               ├─┼┤ ╠═╬╣ ▌▀▄▐<br>
               └─┴┘ ╚═╩╝ ░▒▓</blockquote>''' if not propo else '') + '''
    <p>Includes both uppercase and lowercase underscored and double-struck alphabets, plus superscript and subscript digits:</p>
    <blockquote>
      ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ<br>
      ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ<br>
      𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ<br>
      𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫<br>
      𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡 ⁰¹²³⁴⁵⁶⁷⁸⁹ ₀₁₂₃₄₅₆₇₈₉</blockquote>
    <p>Extensive set of accented Latin letters:</p>
    <blockquote style="word-break: break-all;">ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĆćĈĉĊċĖėĠġĢģĤĥĨĩİıĴĵĶķĹĺĻļŃńŅņŔŕŖŗŚśŜŝŨũŴŵŶŷŸŹźŻżƒǴǵǸǹǼǽǾǿȨȩȮȯ</blockquote>
    <p>Full support for Greek:</p>
    <blockquote>Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϕϖϜϝϲϳϴϵ϶ϷϸϹϼϽϾϿ</blockquote>
    <p>And Cyrillic:</p>
    <blockquote>ЀЁЂЃЄЅІЇЈЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяѐёѓєѕіїјў</blockquote>
    <p>Sample APL code:</p>
    <blockquote style="line-height: 1;"><pre style="font-family: inherit;">''' + ('''
w←⊃(⊃0⍴⍵){                           ⍝┌┌─2─┐       monadic; use ↓
    (e a)←|⍺                         ⍝├ 0 0 1 1 1  dyadic; use /
    T←⌽⍣(0&gt;⊃⌽⍺)                      ⍝└──→⍺⍺←─────┐
    Pad←⍵⍵⍉(T⊣)⍪⍵⍪(T⊢)               ⍝ ┌⍺┐  ⌺     │
    need←(1+e),1↓⍴⍵                  ⍝ ┌─────⍵⍵──┐┘
    a=0:(1↓need⍴0↑⍵)Pad(1↓need⍴0↑⊢⍵) ⍝  0 0│1 2 3 4 5│0 0  Zero
    a=1:(1↓need⍴1↑⍵)Pad(1↓need⍴1↑⊖⍵) ⍝  1 1│1 2 3 4 5│5 5  Replicate
    a=2:(⊖¯1↓need⍴⊢⍵)Pad(¯1↓need⍴⊖⍵) ⍝  2 1│1 2 3 4 5│5 4  Reverse
    a=3:(⊖⊢1↓need⍴⊢⍵)Pad(⊢1↓need⍴⊖⍵) ⍝  3 2│1 2 3 4 5│4 3  Mirror
    a=4:(⊖¯1↓need⍴⊖⍵)Pad(¯1↓need⍴⊢⍵) ⍝  4 5│1 2 3 4 5│1 2  Wrap
}(¯1⌽⍳≢⍴⍵)/(⌽extra,¨⍺⊣0),⊂⍵          ⍝     └────⍵────┘''' if not propo else '''
w←⊃(⊃0⍴⍵){
    (e a)←|⍺
    T←⌽⍣(0&gt;⊃⌽⍺)
    Pad←⍵⍵⍉(T⊣)⍪⍵⍪(T⊢)
    need←(1+e),1↓⍴⍵
    a=0:(1↓need⍴0↑⍵)Pad(1↓need⍴0↑⊢⍵)
    a=1:(1↓need⍴1↑⍵)Pad(1↓need⍴1↑⊖⍵)
    a=2:(⊖¯1↓need⍴⊢⍵)Pad(¯1↓need⍴⊖⍵)
    a=3:(⊖⊢1↓need⍴⊢⍵)Pad(⊢1↓need⍴⊖⍵)
    a=4:(⊖¯1↓need⍴⊖⍵)Pad(¯1↓need⍴⊢⍵)
}(¯1⌽⍳≢⍴⍵)/(⌽extra,¨⍺⊣0),⊂⍵''') + f'''</pre></blockquote>
    <p>Sample text:</p>
    <blockquote>APL (named after the book A Programming Language) is a programming language developed in the 1960s by Kenneth E. Iverson. Its central datatype is the multidimensional array. It uses a large range of special graphic symbols to represent most functions and operators, leading to very concise code. It has been an important influence on the development of concept modeling, spreadsheets, functional programming, and computer math packages. It has also inspired several other programming languages.</blockquote>
  </body>
  <script src="features.js" data-base="{new}"></script>
</html>		 
    ''')

for glyph in apl387.glyphs(): glyph.unlinkRef()

def bake_feature(lookup: str):
  subtable = apl387.getLookupSubtables(lookup)[0]
  to_swap = []
  for glyph in apl387.glyphs():
    lookups = glyph.getPosSub(subtable)
    if len(lookups) == 0: continue
    elif len(lookups) == 1:
      to_swap.append((glyph, apl387.createMappedChar(lookups[0][2])))
    else:
      raise RuntimeError(f'Glyph {glyph.glyphname} has more than one lookup, I don\'t know what to do.')
  for a, b in to_swap:
    swap_glyphs(a, b)
  
temp = apl387.createChar(-1, 'swapTemp')

def swap_glyphs(a, b):
  apl387.selection.select(a)
  apl387.copy()
  apl387.selection.select(temp)
  apl387.paste()
  apl387.selection.select(b)
  apl387.copy()
  apl387.selection.select(a)
  apl387.paste()
  apl387.selection.select(temp)
  apl387.copy()
  apl387.selection.select(b)
  apl387.paste()

def export_all(name, font):
  for subset in powerset(font.gsub_lookups):
    baked_features = [font.getLookupInfo(lookup)[2][0][0] for lookup in subset]
    font.familyname = f'{name} Unicode {" ".join(baked_features)}' if len(subset) else f'{name} Unicode'
    font.fontname = f'{name} Unicode {" ".join(baked_features)}' if len(subset) else f'{name} Unicode'
    file_name = f'{name}-{"-".join(baked_features)}' if len(subset) else name
    for lookup in subset:
      bake_feature(lookup)
    for ext in EXTENSIONS:
      font.generate(f'{path}/output/{file_name}.{ext}')	
    # undo swaps
    for lookup in subset:
      bake_feature(lookup)

export_all('APL387', apl387)
compare_page(apl387, 'APL385', 'APL387')
index_page('APL385', 'APL387')

apl335 = apl387 # no need to clone, original font isn't needed anymore

for glyph in apl335.glyphs():
	if (glyph.glyphname.startswith('part_') # ignore parts
  or glyph.glyphname.endswith('.bottom')  # ignore math components
  or glyph.glyphname.endswith('.top')
  or glyph.glyphname.endswith('.left')
  or glyph.glyphname.endswith('.right')
  or glyph.glyphname.endswith('.extender')
  ): continue 
	glyph.left_side_bearing = 50
	glyph.right_side_bearing = 50
   
apl335.createChar(0x20).left_side_bearing = 200 # space should be wider

apl335.addLookup('kern', 'gpos_pair', (), (('kern', (('DFLT', ('dflt',)), ('brai', ('dflt',)), ('cans', ('dflt',)), ('cyrl', ('dflt',)), ('grek', ('dflt',)), ('latn', ('dflt',)), ('math', ('dflt',)), ('nko ', ('dflt',)), ('tfng', ('dflt',)))),))
apl335.addLookupSubtable('kern', 'kern-0')
with open(f'{path}/kerning.tsv') as kerning:
  reader = csv.reader(kerning, delimiter='\t')
  for line in reader:
    first = apl335.createChar(ord(line[0]))
    second = apl335.createChar(ord(line[1]))
    kern = int(line[2])
    first.addPosSub('kern-0', second.glyphname, kern)

with open(f'{path}/math.toml', 'rb') as math:
  data = tomllib.load(math)
  for k, v in data['properties'].items():
    # font.math doesn't support [] assignment sadly
    exec(f'apl335.math.{k} = {int(v)}', { 'apl335': apl335 })
  for k, v in data['vconstruct'].items():
    glyph = apl335.createMappedChar(k)
    glyph.verticalComponents = tuple(tuple(part) for part in v)
  for k, v in data['hconstruct'].items():
    glyph = apl335.createMappedChar(k)
    glyph.horizontalComponents = tuple(tuple(part) for part in v)

export_all('APL335', apl335)
compare_page(apl335, 'APL333', 'APL335', propo = True, name = 'compare335')
index_page('APL333', 'APL335', propo = True, name = '335', compare_name = 'compare335')
