// Modern Filter Functionality for Projects Page
function filterByCategory(category) {
    const articles = document.getElementsByTagName("article");
    const buttons = document.querySelectorAll('#filter-buttons button');
    
    // Update button states
    buttons.forEach(button => {
        button.classList.remove('active');
        if (button.textContent === category) {
            button.classList.add('active');
        }
    });
    
    // Filter articles with smooth animation
    for (let i = 0; i < articles.length; i++) {
        const categories = articles[i].getAttribute("category").split(", ");
        
        if (categories.includes(category) || category === 'All') {
            articles[i].style.display = "block";
            articles[i].style.opacity = "0";
            articles[i].style.transform = "translateY(20px)";
            
            // Smooth fade-in animation
            setTimeout(() => {
                articles[i].style.transition = "opacity 0.3s ease, transform 0.3s ease";
                articles[i].style.opacity = "1";
                articles[i].style.transform = "translateY(0)";
            }, 50);
        } else {
            // Smooth fade-out animation
            articles[i].style.transition = "opacity 0.3s ease, transform 0.3s ease";
            articles[i].style.opacity = "0";
            articles[i].style.transform = "translateY(-20px)";
            
            setTimeout(() => {
                articles[i].style.display = "none";
            }, 300);
        }
    }
    
}


// Initialize filter on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set initial active state
    const allButton = document.querySelector('#filter-buttons button');
    if (allButton) {
        allButton.classList.add('active');
    }
    
    // Add hover effects to filter buttons
    const buttons = document.querySelectorAll('#filter-buttons button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            }
        });
    });
    
});

// Add smooth scrolling for better UX
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Add keyboard navigation for filter buttons
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        const buttons = document.querySelectorAll('#filter-buttons button');
        const activeIndex = Array.from(buttons).findIndex(btn => btn.classList.contains('active'));
        
        switch(e.key) {
            case '1':
                e.preventDefault();
                filterByCategory('All');
                break;
            case '2':
                e.preventDefault();
                filterByCategory('LLM & Deep Learning');
                break;
            case '3':
                e.preventDefault();
                filterByCategory('NLP');
                break;
            case '4':
                e.preventDefault();
                filterByCategory('Forecasting');
                break;
            case '5':
                e.preventDefault();
                filterByCategory('ML');
                break;
            case '6':
                e.preventDefault();
                filterByCategory('Others');
                break;
        }
    }
});