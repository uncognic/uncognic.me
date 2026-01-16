(function () {
    function insertHeader(html) {
        var el = document.getElementById('site-header');
        if (!el) {
            el = document.createElement('div');
            el.id = 'site-header';
            el.setAttribute('aria-hidden', 'true');
            document.body.insertBefore(el, document.body.firstChild);
        }
        el.innerHTML = html;
    }

    var partialPath = '/partials/header.html';
    fetch(partialPath, { cache: 'no-cache' }).then(function (r) {
        if (!r.ok) throw new Error('Failed to load header');
        return r.text();
    }).then(insertHeader).catch(function (err) {
    });
})();