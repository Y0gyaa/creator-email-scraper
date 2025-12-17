// API Base URL
const API_BASE = 'http://localhost:5000';

// State
let currentResults = [];

// DOM Elements
const searchForm = document.getElementById('searchForm');
const searchBtn = document.getElementById('searchBtn');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const emptyState = document.getElementById('emptyState');
const resultsBody = document.getElementById('resultsBody');
const resultCount = document.getElementById('resultCount');
const exportBtn = document.getElementById('exportBtn');

// Event Listeners
searchForm.addEventListener('submit', handleSearch);
exportBtn.addEventListener('click', handleExport);

/**
 * Handle search form submission
 */
async function handleSearch(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(searchForm);
    const searchParams = {
        niche: formData.get('niche'),
        country: formData.get('country'),
        city: formData.get('city'),
        area: formData.get('area'),
        max_results: parseInt(formData.get('maxResults')) || 50
    };
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchParams)
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentResults = data.results;
            displayResults(data.results);
        } else {
            showError(data.error || 'An error occurred during search');
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to connect to server. Please make sure the backend is running.');
    }
}

/**
 * Display results in the table
 */
function displayResults(results) {
    // Hide loading and empty state
    loadingState.style.display = 'none';
    emptyState.style.display = 'none';
    
    if (results.length === 0) {
        resultsSection.style.display = 'none';
        emptyState.style.display = 'block';
        const emptyStateText = emptyState.querySelector('p');
        emptyStateText.textContent = 'No results found. Try different search criteria.';
        return;
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    resultCount.textContent = results.length;
    
    // Clear existing results
    resultsBody.innerHTML = '';
    
    // Populate table
    results.forEach(result => {
        const row = document.createElement('tr');
        
        // Build location string
        const locationParts = [];
        if (result.city) locationParts.push(result.city);
        if (result.country) locationParts.push(result.country);
        if (result.area && !locationParts.includes(result.area)) locationParts.push(result.area);
        const location = locationParts.join(', ') || 'N/A';
        
        row.innerHTML = `
            <td>${escapeHtml(result.name || 'Unknown')}</td>
            <td><a href="mailto:${escapeHtml(result.email)}">${escapeHtml(result.email)}</a></td>
            <td><span class="platform-badge">${escapeHtml(result.platform || 'Web')}</span></td>
            <td>${escapeHtml(result.niche || 'N/A')}</td>
            <td>${escapeHtml(location)}</td>
            <td><a href="${escapeHtml(result.url)}" target="_blank" rel="noopener noreferrer">View</a></td>
        `;
        
        resultsBody.appendChild(row);
        
        // Add fade-in animation
        row.style.opacity = '0';
        setTimeout(() => {
            row.style.transition = 'opacity 0.3s ease';
            row.style.opacity = '1';
        }, 10);
    });
}

/**
 * Show loading state
 */
function showLoading() {
    loadingState.style.display = 'block';
    resultsSection.style.display = 'none';
    emptyState.style.display = 'none';
    searchBtn.disabled = true;
    searchBtn.innerHTML = `
        <div style="width: 20px; height: 20px; border: 2px solid white; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        Searching...
    `;
}

/**
 * Show error message
 */
function showError(message) {
    loadingState.style.display = 'none';
    resultsSection.style.display = 'none';
    emptyState.style.display = 'block';
    searchBtn.disabled = false;
    searchBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
        </svg>
        Search Creators
    `;
    
    const emptyStateText = emptyState.querySelector('p');
    emptyStateText.textContent = message;
    emptyStateText.style.color = '#ff4757';
}

/**
 * Handle CSV export
 */
async function handleExport() {
    if (currentResults.length === 0) {
        alert('No results to export');
        return;
    }
    
    exportBtn.disabled = true;
    exportBtn.innerHTML = `
        <div style="width: 20px; height: 20px; border: 2px solid currentColor; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        Exporting...
    `;
    
    try {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const filename = `creators_${timestamp}.csv`;
        
        const response = await fetch(`${API_BASE}/api/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                results: currentResults,
                filename: filename
            })
        });
        
        if (response.ok) {
            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            alert('Failed to export results');
        }
    } catch (error) {
        console.error('Export error:', error);
        alert('Failed to export results');
    } finally {
        exportBtn.disabled = false;
        exportBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Export CSV
        `;
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Content Creator Email Scraper initialized');
});
