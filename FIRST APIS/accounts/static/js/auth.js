function isAuthenticated() {
    return localStorage.getItem('access_token') !== null;
}

function checkAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login/';
    }
}

function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    
    if (!refreshToken) {
        throw new Error('No refresh token available');
    }

    try {
        const response = await fetch('/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return data.access;
        } else {
            throw new Error('Token refresh failed');
        }
    } catch (error) {
        logout();
        throw error;
    }
}

async function fetchWithAuth(url, options = {}) {
    let token = getAccessToken();
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    try {
        let response = await fetch(url, mergedOptions);

        if (response.status === 401) {
            token = await refreshAccessToken();
            mergedOptions.headers.Authorization = `Bearer ${token}`;
            response = await fetch(url, mergedOptions);
        }

        const data = await response.json();

        if (response.ok) {
            return data;
        } else {
            throw data;
        }
    } catch (error) {
        throw error;
    }
}

async function logout() {
    try {
        const refreshToken = getRefreshToken();
        
        if (refreshToken) {
            await fetchWithAuth('/api/logout/', {
                method: 'POST',
                body: JSON.stringify({ refresh: refreshToken })
            });
        }
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        
        window.location.href = '/login/';
    }
}