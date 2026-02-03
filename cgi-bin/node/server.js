const http = require('http');
const url = require('url');
const os = require('os');
const fs = require('fs');

const SESSION_DIR = '/tmp/node_sessions';
if (!fs.existsSync(SESSION_DIR)) fs.mkdirSync(SESSION_DIR);

// ── Session helpers ──
function getSessionId(headers) {
    const cookies = (headers.cookie || '').split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'NODE_SID') return value;
    }
    return null;
}

function loadSession(sid) {
    const file = `${SESSION_DIR}/${sid}.json`;
    if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file));
    return {};
}

function saveSession(sid, data) {
    fs.writeFileSync(`${SESSION_DIR}/${sid}.json`, JSON.stringify(data));
}

function deleteSession(sid) {
    const file = `${SESSION_DIR}/${sid}.json`;
    if (fs.existsSync(file)) fs.unlinkSync(file);
}

function generateId() {
    return require('crypto').randomBytes(16).toString('hex');
}

// ── Parse body ──
function getBody(req) {
    return new Promise((resolve) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => resolve(body));
    });
}

// ── Routes ──
async function handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;

    // hello-html
    if (path === '/cgi-bin/node/hello-html-node') {
        res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-cache' });
        res.end(`<!DOCTYPE html>
<html><head><title>Hello CGI World</title></head>
<body>
<h1 align="center">Hello HTML World</h1><hr>
<p>Hello Andre!</p>
<p>This page was generated with the Node.js programming language</p>
<p>This program was generated at: ${new Date()}</p>
<p>Your current IP Address is: ${req.headers['x-forwarded-for'] || req.socket.remoteAddress}</p>
</body></html>`);
        return;
    }

    // hello-json
    if (path === '/cgi-bin/node/hello-json-node') {
        res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache' });
        res.end(JSON.stringify({
            greeting: "Hello Andre!",
            language: "Node.js",
            generated_at: new Date().toString(),
            ip_address: req.headers['x-forwarded-for'] || req.socket.remoteAddress
        }, null, 2));
        return;
    }

    // environment
    if (path === '/cgi-bin/node/environment-node') {
        res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-cache' });
        const vars = { ...process.env, ...{
            REQUEST_METHOD: req.method,
            REQUEST_URI: req.url,
            SERVER_PROTOCOL: `HTTP/${req.httpVersion}`,
            HTTP_HOST: req.headers.host,
            REMOTE_ADDR: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
            HTTP_USER_AGENT: req.headers['user-agent']
        }};
        let rows = Object.keys(vars).sort().map(k => `<b>${k}:</b> ${vars[k]}<br />`).join('\n');
        res.end(`<!DOCTYPE html>
<html><head><title>Environment Variables</title></head>
<body><h1 align="center">Environment Variables</h1><hr>
${rows}
</body></html>`);
        return;
    }

    // echo
    if (path === '/cgi-bin/node/echo-node') {
        const body = await getBody(req);
        const contentType = req.headers['content-type'] || '';
        let parsed = {};
        if (body) {
            if (contentType.includes('application/json')) {
                try { parsed = JSON.parse(body); } catch(e) { parsed = { error: 'Invalid JSON' }; }
            } else {
                const params = new URLSearchParams(body);
                params.forEach((v, k) => parsed[k] = v);
            }
        }
        // Also parse query string for GET
        if (req.method === 'GET' && parsedUrl.query) {
            parsed = { ...parsedUrl.query };
        }

        res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-cache' });
        res.end(`<!DOCTYPE html>
<html><head><title>Echo Request</title></head>
<body>
<h1 align="center">Echo Request</h1><hr>
<p><b>Hostname:</b> ${os.hostname()}</p>
<p><b>Date/Time:</b> ${new Date()}</p>
<p><b>User Agent:</b> ${req.headers['user-agent']}</p>
<p><b>IP Address:</b> ${req.headers['x-forwarded-for'] || req.socket.remoteAddress}</p>
<hr>
<p><b>HTTP Method:</b> ${req.method}</p>
<p><b>Content-Type:</b> ${contentType}</p>
<p><b>Query String:</b> ${parsedUrl.query ? JSON.stringify(parsedUrl.query) : ''}</p>
<p><b>Message Body:</b> ${body}</p>
<hr>
<h2>Parsed Data</h2>
<ul>${Object.keys(parsed).map(k => `<li><b>${k}:</b> ${parsed[k]}</li>`).join('\n') || '<li>No data</li>'}
</ul>
</body></html>`);
        return;
    }

    // state - save
    if (path === '/cgi-bin/node/state-node-save') {
        let sid = getSessionId(req.headers);
        if (!sid) sid = generateId();
        let session = loadSession(sid);

        if (req.method === 'POST') {
            const body = await getBody(req);
            const params = new URLSearchParams(body);
            session.name = params.get('name') || session.name;
            session.message = params.get('message') || session.message;
            session.saved_at = new Date().toString();
            saveSession(sid, session);
        }

        res.writeHead(200, {
            'Content-Type': 'text/html',
            'Cache-Control': 'no-cache',
            'Set-Cookie': `NODE_SID=${sid}; path=/`
        });
        res.end(`<!DOCTYPE html>
<html><head><title>State - Save Data</title></head>
<body>
<h1 align="center">State Demo - Save Data</h1><hr>
<form method="POST" action="/cgi-bin/node/state-node-save">
    <label>Name: </label><input type="text" name="name" value="${session.name || ''}" /><br /><br />
    <label>Message: </label><input type="text" name="message" value="${session.message || ''}" /><br /><br />
    <input type="submit" value="Save" />
</form>
<hr>
<p><a href="/cgi-bin/node/state-node-view">View saved data</a></p>
<p><a href="/cgi-bin/node/state-node-clear">Clear session</a></p>
</body></html>`);
        return;
    }

    // state - view
    if (path === '/cgi-bin/node/state-node-view') {
        const sid = getSessionId(req.headers);
        const session = sid ? loadSession(sid) : {};

        res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-cache' });
        res.end(`<!DOCTYPE html>
<html><head><title>State - View Data</title></head>
<body>
<h1 align="center">State Demo - View Data</h1><hr>
${session.name ? `
<p><b>Name:</b> ${session.name}</p>
<p><b>Message:</b> ${session.message}</p>
<p><b>Saved at:</b> ${session.saved_at}</p>` : '<p>No data saved yet. Go save some!</p>'}
<hr>
<p><a href="/cgi-bin/node/state-node-save">Go back and edit</a></p>
<p><a href="/cgi-bin/node/state-node-clear">Clear session</a></p>
</body></html>`);
        return;
    }

    // state - clear
    if (path === '/cgi-bin/node/state-node-clear') {
        const sid = getSessionId(req.headers);
        if (sid) deleteSession(sid);

        res.writeHead(200, {
            'Content-Type': 'text/html',
            'Cache-Control': 'no-cache',
            'Set-Cookie': 'NODE_SID=; max-age=0; path=/'
        });
        res.end(`<!DOCTYPE html>
<html><head><title>State - Session Cleared</title></head>
<body>
<h1 align="center">Session Cleared</h1><hr>
<p>Your session data has been deleted.</p>
<p><a href="/cgi-bin/node/state-node-save">Back to Save Page</a></p>
<p><a href="/cgi-bin/node/state-node-view">Back to View Page</a></p>
</body></html>`);
        return;
    }

    // 404 for anything else
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end('<h1>404 - Not Found</h1>');
}

// ── Start server ──
const PORT = 3000;
http.createServer(handleRequest).listen(PORT, () => {
    console.log(`Node CGI server running on port ${PORT}`);
});
