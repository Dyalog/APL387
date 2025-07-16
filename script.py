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

with open(f'{path}/output/index.html', 'w', encoding='utf-8') as index:
	features = [apl387.getLookupInfo(lookup)[2][0][0] for lookup in apl387.gsub_lookups]

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
    <h1>APL387 Unicode<sup> <a href="APL387.ttf">download</a></sup><span><sup><a href="https://github.com/dyalog/APL387">source</a></sup></span></h1>
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
	<script>
		const styles = new Map([...document.querySelectorAll('[type=checkbox]')].map(e => [e.value, e]));
		for (const [set, element] of styles.entries()) {
			element.addEventListener('input', () => {
        const settings = [...styles.entries()].flatMap(([s, e]) => e.checked ? ['"' + s + '"'] : []).join(', ');
				document.body.style.fontFeatureSettings = settings.trim().length ? settings : 'unset';
			});
		}
	</script>
</html>		 
	''')

for ext in EXTENSIONS:
	apl387.generate(f'{path}/output/APL387.{ext}')	
