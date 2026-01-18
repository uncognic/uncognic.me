(function () {
    function insertAbout(html) {
        var el = document.getElementById('site-about');
        if (!el) {
            el = document.createElement('div');
            el.id = 'site-about';
            el.setAttribute('aria-hidden', 'true');
            document.body.insertBefore(el, document.body.firstChild);
        }
        el.innerHTML = html;
    }

    var partialPath = '/partials/about.html';
    fetch(partialPath, { cache: 'no-cache' }).then(function (r) {
        if (!r.ok) throw new Error('Failed to load about partial');
        return r.text();
    }).then(function(html){
        var el = document.getElementById('site-about');
        if (el) {
            el.outerHTML = html;
        } else {
            insertAbout(html);
        }
    }).catch(function (err) {
    });
})();