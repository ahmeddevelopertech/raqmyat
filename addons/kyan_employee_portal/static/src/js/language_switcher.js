// Function to change language and update URL
function setupLanguageSwitcher() {
    const languageSelector = document.getElementById('language-selector');
    
    // Set initial value based on current URL
    const currentPath = window.location.pathname;
    const currentLang = currentPath.split('/')[1];
    if (currentLang === 'ar') {
        languageSelector.value = 'ar_001';
    } else {
        languageSelector.value = 'en_US';
    }

    languageSelector.addEventListener('change', function(e) {
        const selectedLang = e.target.value;
        let newPrefix = 'en';
        
        if (selectedLang === 'ar_001') {
            newPrefix = 'ar';
        }
        
        // Get current URL path parts
        const pathParts = window.location.pathname.split('/');
        
        // Check if first part after / is a language code
        if (pathParts[1] === 'ar' || pathParts[1] === 'en') {
            // Replace existing language code
            pathParts[1] = newPrefix;
        } else {
            // Insert language code if none exists
            pathParts.splice(1, 0, newPrefix);
        }
        
        // Reconstruct URL with query parameters if they exist
        const newPath = pathParts.join('/');
        const newUrl = newPath + window.location.search + window.location.hash;
        
        // Redirect to new URL
        window.location.href = newUrl;
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', setupLanguageSwitcher);