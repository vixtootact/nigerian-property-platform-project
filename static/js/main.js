const API = 'http://127.0.0.1:8000/api';


function saveUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function logoutUser() {
    localStorage.removeItem('user');
    window.location.href = '/';
}

function isLoggedIn() {
    return getUser() !== null;
}

function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = '/login/';
    }
}

function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = '/dashboard/';
    }
}


async function apiGet(endpoint) {
    try {
        const response = await fetch(`${API}${endpoint}`);
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: 'Network error. Is the server running?' } };
    }
}

async function apiPost(endpoint, body) {
    try {
        const response = await fetch(`${API}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: 'Network error. Is the server running?' } };
    }
}

async function apiPut(endpoint, body) {
    try {
        const response = await fetch(`${API}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: 'Network error. Is the server running?' } };
    }
}

async function apiDelete(endpoint) {
    try {
        const response = await fetch(`${API}${endpoint}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: 'Network error. Is the server running?' } };
    }
}


function formatPrice(price) {
    return '₦' + Number(price).toLocaleString('en-NG');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-NG', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function statusBadge(status) {
    return `<span class="badge badge-${status}">${status}</span>`;
}

function propertyIcon(type) {
    const icons = {
        'apartment':    '🏢',
        'duplex':       '🏠',
        'bungalow':     '🏡',
        'self-contain': '🏘️',
        'room':         '🛏️',
        'mansion':      '🏰'
    };
    return icons[type] || '🏠';
}


function buildNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    const user = getUser();

    let links = `
        <li><a href="/properties/">Properties</a></li>
        <li><a href="/login/">Login</a></li>
        <li><a href="/register/" class="btn-nav">Register</a></li>
    `;

    if (user) {
        links = `
            <li><a href="/properties/">Properties</a></li>
            <li><a href="/dashboard/">Dashboard</a></li>
            <li><a href="/profile/">👤 ${user.first_name}</a></li>
            <li><a href="#" onclick="logoutUser()" class="btn-nav">Logout</a></li>
        `;
    }

    navbar.innerHTML = `
        <a href="/" class="navbar-brand">🏠 Naija<span>Homes</span></a>
        <ul class="navbar-links">${links}</ul>
    `;
}


function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = message;
        el.className = 'alert alert-error';
        el.style.display = 'block';
    }
}

function showSuccess(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = message;
        el.className = 'alert alert-success';
        el.style.display = 'block';
    }
}

function hideAlert(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.style.display = 'none';
}


function getParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}


document.addEventListener('DOMContentLoaded', buildNavbar);