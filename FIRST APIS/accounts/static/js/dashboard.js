checkAuth();

const loading = document.getElementById('loading');
const dashboardContent = document.getElementById('dashboard-content');

async function loadDashboard() {
    try {
        const userData = await fetchWithAuth('/api/user/');
        const user = userData.user;
        
        document.getElementById('user-name').textContent = user.first_name;
        document.getElementById('user-email').textContent = user.email;
        document.getElementById('user-id').textContent = user.id;
        document.getElementById('username').textContent = user.username;
        document.getElementById('email').textContent = user.email;
        document.getElementById('full-name').textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById('date-joined').textContent = new Date(user.date_joined).toLocaleDateString();
        
        await loadProtectedData();
        
        loading.style.display = 'none';
        dashboardContent.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        alert('Failed to load dashboard data');
    }
}

async function loadProtectedData() {
    try {
        const protectedDataDiv = document.getElementById('protected-data');
        protectedDataDiv.innerHTML = '<p>Loading...</p>';
        
        const data = await fetchWithAuth('/api/protected/');
        
        protectedDataDiv.innerHTML = `
            <p><strong>Message:</strong> ${data.message}</p>
            <p><strong>User:</strong> ${data.user}</p>
            <p><strong>User ID:</strong> ${data.user_id}</p>
            <p><strong>Info:</strong> ${data.data.info}</p>
        `;
    } catch (error) {
        document.getElementById('protected-data').innerHTML = 
            '<p style="color: red;">Failed to load protected data</p>';
    }
}

document.getElementById('logout-btn').addEventListener('click', logout);
document.getElementById('fetch-protected-btn').addEventListener('click', loadProtectedData);

loadDashboard();