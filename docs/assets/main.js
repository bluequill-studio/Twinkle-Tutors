// Mobile nav
document.querySelector('.nav-toggle')?.addEventListener('click', () => {
  document.body.classList.toggle('nav-open');
});
document.querySelectorAll('.menu > li > button').forEach((btn) => {
  btn.addEventListener('click', () => {
    if (window.matchMedia('(max-width: 1080px)').matches) btn.parentElement.classList.toggle('open');
  });
});

// Forms post to data-endpoint (e.g. Formspree) when set, otherwise to Netlify Forms; locally they just show the success message.
document.querySelectorAll('form[data-demo-form]').forEach((form) => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    const local = ['localhost', '127.0.0.1'].includes(location.hostname);
    if (!local) {
      try {
        const endpoint = form.dataset.endpoint;
        const res = endpoint
          ? await fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
          : await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(new FormData(form)).toString(),
          });
        if (!res.ok) throw new Error(res.status);
      } catch (err) {
        alert('Sorry, something went wrong. Please try again or email us.');
        return;
      }
    }
    form.classList.add('sent');
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
});

// Pricing: weekly vs. term billing
const toggle = document.querySelector('[data-billing]');
if (toggle) {
  toggle.querySelectorAll('button').forEach((b) => {
    b.addEventListener('click', () => {
      toggle.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
      const mode = b.dataset.mode;
      document.querySelectorAll('[data-weekly]').forEach((el) => {
        el.textContent = mode === 'term' ? el.dataset.term : el.dataset.weekly;
      });
      const termUnit = toggle.dataset.termUnit || '/session, paid per term';
      document.querySelectorAll('[data-unit]').forEach((el) => {
        el.textContent = mode === 'term' ? termUnit : '/session';
      });
    });
  });
}

// Blog category filter
const filters = document.querySelector('.filters');
if (filters) {
  filters.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    filters.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    document.querySelectorAll('.post').forEach((p) => {
      p.style.display = b.dataset.cat === 'all' || p.dataset.cat === b.dataset.cat ? '' : 'none';
    });
  });
}

// Pre-fill free trial subject from ?subject= / ?exam=
const params = new URLSearchParams(location.search);
const pre = params.get('subject') || params.get('exam');
const sel = document.querySelector('#trial-subject');
if (pre && sel) {
  [...sel.options].forEach((o) => { if (o.value === pre) sel.value = pre; });
}

document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
