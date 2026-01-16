async function loadInfo() {
            try {
                const res = await fetch('https://ipinfo.io/json');
                const j = await res.json();

                document.getElementById('pub-ip').textContent = j.ip || 'unknown';
                document.getElementById('hostname').textContent = j.hostname || 'unknown';
                document.getElementById('org').textContent = j.org || 'unknown';
                document.getElementById('city').textContent = j.city || 'unknown';
                document.getElementById('region').textContent = j.region || 'unknown';
                document.getElementById('country').textContent = j.country || 'unknown';
                document.getElementById('loc').textContent = j.loc || 'unknown';
                document.getElementById('postal').textContent = j.postal || 'unknown';
                document.getElementById('timezone').textContent = j.timezone || 'unknown';
            } catch (e) {
                ['pub-ip','hostname','org','city','region','country','loc','postal','timezone'].forEach(id => {
                    document.getElementById(id).textContent = 'error';
                });
            }

            document.getElementById('ua').textContent = navigator.userAgent || 'n/a';
        }
        loadInfo();