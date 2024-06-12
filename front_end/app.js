// base_url_api = `http://127.0.0.1:8040`
base_url_api = `https://test-deploy-web-to-vercel-backend.vercel.app`

async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch(`${base_url_api}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const result = await response.json();
        alert(result.message);
    } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch(`${base_url_api}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const result = await response.json();
        alert(result.message);
    } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
    }
}
