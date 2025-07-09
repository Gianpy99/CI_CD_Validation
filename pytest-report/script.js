
// Coverage-style JavaScript for pytest report
document.addEventListener('DOMContentLoaded', function() {
    // Auto-expand failed tests
    const failedRows = document.querySelectorAll('tr[data-status="failed"]');
    failedRows.forEach(row => {
        const details = row.querySelector('.test-details');
        if (details) {
            details.classList.add('show');
        }
    });
    
    // Filter functionality
    const filterInput = document.getElementById('filter');
    if (filterInput) {
        filterInput.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const testName = row.querySelector('.test-name').textContent.toLowerCase();
                if (testName.includes(filterValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Hide passed tests checkbox
    const hidePassedCheckbox = document.getElementById('hide-passed');
    if (hidePassedCheckbox) {
        hidePassedCheckbox.addEventListener('change', function() {
            const passedRows = document.querySelectorAll('tr[data-status="passed"]');
            passedRows.forEach(row => {
                row.style.display = this.checked ? 'none' : '';
            });
        });
    }
});

function toggleDetails(index) {
    const details = document.getElementById('details-' + index);
    if (details) {
        details.classList.toggle('show');
    }
}

function toggleAllDetails() {
    const allDetails = document.querySelectorAll('.test-details');
    const anyVisible = Array.from(allDetails).some(detail => detail.classList.contains('show'));
    
    allDetails.forEach(detail => {
        if (anyVisible) {
            detail.classList.remove('show');
        } else {
            detail.classList.add('show');
        }
    });
}
