const withBakedDownload = document.querySelector('#wb');

const styles = new Map([...document.querySelectorAll('[type=checkbox]')].map(e => [e.value, e]));
for (const element of styles.values()) {
	element.addEventListener('input', () => {
		const settings = [...styles.entries()].flatMap(([s, e]) => e.checked ? ['"' + s + '"'] : []).join(', ');
		document.body.style.fontFeatureSettings = settings.trim().length ? settings : 'unset';
		withBakedDownload.href = `APL387-${settings.replaceAll(', ', '-').replaceAll('"', '')}.ttf`;
		if (settings.trim().length) withBakedDownload.classList.add('s');
		else withBakedDownload.classList.remove('s');
	});
}
