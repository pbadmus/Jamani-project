// Main JavaScript functionality for the birthday website
document.addEventListener('DOMContentLoaded', function() {
    console.log('Birthday website loaded successfully!');
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading animation for video uploads
    const videoForms = document.querySelectorAll('form[enctype="multipart/form-data"]');
    videoForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.textContent = 'Uploading...';
                submitBtn.disabled = true;
            }
        });
    });
});