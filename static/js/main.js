document.addEventListener('DOMContentLoaded', function() {
    // Animation for elements that should fade in
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.classList.add('fade-in');
    });
    
    // Animation for elements that should slide in
    const slideElements = document.querySelectorAll('.slide-in');
    slideElements.forEach(element => {
        element.classList.add('slide-in');
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Initialize any tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize datepicker for booking forms if available
    if (typeof flatpickr !== 'undefined') {
        flatpickr('.datepicker', {
            enableTime: false,
            dateFormat: 'Y-m-d',
            minDate: 'today'
        });
    }
    
    // Enhance select inputs with Select2 if available
    if (typeof $.fn.select2 !== 'undefined') {
        $('.select2').select2({
            theme: 'bootstrap-5'
        });
    }
    
    // Handle booking date selection
    const tourDateSelect = document.getElementById('id_tour_date');
    const priceDisplay = document.getElementById('tour-price');
    const numberOfPeopleInput = document.getElementById('id_number_of_people');
    const totalPriceDisplay = document.getElementById('total-price');
    
    if (tourDateSelect && priceDisplay && numberOfPeopleInput && totalPriceDisplay) {
        const updateTotalPrice = () => {
            const selectedOption = tourDateSelect.options[tourDateSelect.selectedIndex];
            const price = parseFloat(selectedOption.getAttribute('data-price') || 0);
            const numberOfPeople = parseInt(numberOfPeopleInput.value) || 1;
            
            priceDisplay.textContent = '$' + price.toFixed(2);
            totalPriceDisplay.textContent = '$' + (price * numberOfPeople).toFixed(2);
        };
        
        tourDateSelect.addEventListener('change', updateTotalPrice);
        numberOfPeopleInput.addEventListener('change', updateTotalPrice);
        numberOfPeopleInput.addEventListener('input', updateTotalPrice);
        
        // Initialize with default values
        updateTotalPrice();
    }
    
    // Handle participant form fields dynamically
    const addParticipantBtn = document.getElementById('add-participant');
    if (addParticipantBtn) {
        addParticipantBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const participantForms = document.querySelectorAll('.participant-form');
            const totalForms = document.getElementById('id_participants-TOTAL_FORMS');
            const formNum = participantForms.length;
            
            // Clone the first form
            const newForm = participantForms[0].cloneNode(true);
            
            // Update form index
            newForm.innerHTML = newForm.innerHTML.replace(/-0-/g, `-${formNum}-`);
            newForm.innerHTML = newForm.innerHTML.replace(/_0_/g, `_${formNum}_`);
            
            // Clear form values
            const inputs = newForm.querySelectorAll('input, textarea');
            inputs.forEach(input => {
                input.value = '';
            });
            
            // Add new form to container
            document.getElementById('participants-container').appendChild(newForm);
            
            // Update total forms
            totalForms.value = formNum + 1;
        });
    }
    
    // Initialize charts for the dashboard if Chart.js is available
    if (typeof Chart !== 'undefined' && document.getElementById('bookingChart')) {
        // Sample booking chart
        const bookingCtx = document.getElementById('bookingChart').getContext('2d');
        new Chart(bookingCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Bookings',
                    data: [65, 59, 80, 81, 56, 55, 40, 45, 60, 70, 80, 90],
                    fill: false,
                    borderColor: '#38a169',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Sample revenue chart
        const revenueCtx = document.getElementById('revenueChart').getContext('2d');
        new Chart(revenueCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue',
                    data: [1500, 1900, 3000, 5000, 2000, 3000, 4000, 4500, 6000, 7000, 8000, 9000],
                    backgroundColor: '#2c7a7b'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});