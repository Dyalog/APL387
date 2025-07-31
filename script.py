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
commit = sys.argv[2]

apl387 = fontforge.open(f'{path}/APL387.ufo2')

apl387.version = commit

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

with open(f'{path}/output/compare.html', 'w', encoding='utf-8') as compare:
	compare.write('''
<html lang="en">
  <head>
    <meta charset="utf-8" /> 
    <title>APL387 Comparison</title>
    <style>
@font-face {font-family: 'APL387';src: url('APL387.ttf');}
@font-face {font-family: 'APL385';src: url('APL385.ttf');}
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
#APL385{font-family:APL385!important}
#APL387{font-family:APL387!important}
</style>
  </head>
  <body>
	''')
	for feature in features:
		compare.write(f'<input id="{feature}" type="checkbox" name="{feature}" value="{feature}"><label for="{feature}">{feature}</label>')
	compare.write('<br><a href="../chars">compare characters individually</a>')
	same = '''
<textarea id="ta385" placeholder="Try it yourself ― type here!" spellcheck="false" oninput"ta387.value=this.value"></textarea>
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
    </blockquote>
    <p>Single and double line drawing characters, and blocks and shades:</p>
    <blockquote style="line-height: 1.15;">┌─┬┐ ╔═╦╗ ▁▂▃▄▅▆▇█<br>
               │ ││ ║ ║║ █▉▊▋▌▍▎▏<br>
               ├─┼┤ ╠═╬╣ ▌▀▄▐<br>
               └─┴┘ ╚═╩╝ ░▒▓</blockquote>
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
    <blockquote style="line-height: 1;"><pre style="font-family: inherit;">
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
}(¯1⌽⍳≢⍴⍵)/(⌽extra,¨⍺⊣0),⊂⍵          ⍝     └────⍵────┘</pre></blockquote>
    <p>Sample text:</p>
    <blockquote>APL (named after the book A Programming Language) is a programming language developed in the 1960s by Kenneth E. Iverson. Its central datatype is the multidimensional array. It uses a large range of special graphic symbols to represent most functions and operators, leading to very concise code. It has been an important influence on the development of concept modeling, spreadsheets, functional programming, and computer math packages. It has also inspired several other programming languages.</blockquote>
<p>All supported characters:</p>
<pre>
	'''
	for idx, gl in enumerate(sorted((gl for gl in apl387.glyphs() if gl.unicode != -1), key=lambda gl: gl.unicode)):
		if idx != 0 and idx % 16 == 0: same += '\n'
		same += f'&#{gl.unicode};'
	same += '</pre>'
	compare.write(f'''
<div>
<section id='APL385'><h2>APL385 Unicode</h2>
	{same}
</section>
<section id='APL387'><h2>New APL387 Unicode</h2>
	{same}
</section>
</div>
	<script src="features.js"></script>
  </body>
</html>
	''')

with open(f'{path}/output/index.html', 'w', encoding='utf-8') as index:
	index.write('''
<html lang="en">
  <head>
    <meta charset="utf-8" /> 
    <title>APL387 - A New APL385</title>
    <link rel="shortcut icon" href="favicon.ico"/>
    <link rel="stylesheet" href="index.css">
  </head>
  <body>
		<div class="c">
      <input id="APL387" class="x" type="radio" name="f" value="APL387" checked=""><label class="x" for="APL387">APL387.ttf</label>
      <input id="APL385" class="x" type="radio" name="f" value="APL385"            ><label class="x" for="APL385">APL385.ttf</label>
			<br>
	''')
	for feature in features:
		index.write(f'<input id="{feature}" type="checkbox" name="{feature}" value="{feature}"><label for="{feature}">{feature}</label>')
	index.write('''
		</div>
    <h1>APL387 Unicode<sup> <a href="APL387.ttf">download</a></sup> <span><sup><a href="./compare">side by side with APL385</a></sup> <sup><a href="https://github.com/dyalog/APL387">source</a></sup></span></h1>
    <p>A redrawn and extended version of Adrian Smith's classic <a href="https://apl385.com/fonts/index.htm">APL385</a> font with clean rounded look.</p>
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
    </blockquote>
    <p>Single and double line drawing characters, and blocks and shades:</p>
    <blockquote style="line-height: 1.15;">┌─┬┐ ╔═╦╗ ▁▂▃▄▅▆▇█<br>
               │ ││ ║ ║║ █▉▊▋▌▍▎▏<br>
               ├─┼┤ ╠═╬╣ ▌▀▄▐<br>
               └─┴┘ ╚═╩╝ ░▒▓</blockquote>
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
    <blockquote style="line-height: 1;"><pre style="font-family: inherit;">
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
}(¯1⌽⍳≢⍴⍵)/(⌽extra,¨⍺⊣0),⊂⍵          ⍝     └────⍵────┘</pre></blockquote>
    <p>Sample text:</p>
    <blockquote>APL (named after the book A Programming Language) is a programming language developed in the 1960s by Kenneth E. Iverson. Its central datatype is the multidimensional array. It uses a large range of special graphic symbols to represent most functions and operators, leading to very concise code. It has been an important influence on the development of concept modeling, spreadsheets, functional programming, and computer math packages. It has also inspired several other programming languages.</blockquote>
  </body>
	<script src="features.js"></script>
</html>		 
	''')

for ext in EXTENSIONS:
	apl387.generate(f'{path}/output/APL387.{ext}')	
