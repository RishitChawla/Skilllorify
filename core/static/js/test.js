document.addEventListener('DOMContentLoaded', function() {
    // Handle option selection
    const optionInputs = document.querySelectorAll('.option-input');
    
    optionInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Mark question as answered in navigation
            const questionDot = document.querySelector('.question-dot.active');
            if (questionDot) {
                questionDot.classList.add('answered');
            }
        });
    });
    
    // Handle navigation dots
    const questionDots = document.querySelectorAll('.question-dot');
    
    questionDots.forEach(dot => {
        dot.addEventListener('click', function() {
            // In a real implementation, this would navigate to the selected question
            // For demo purposes, we'll just update the active state
            
            // Remove active class from current active dot
            const activeDot = document.querySelector('.question-dot.active');
            if (activeDot) {
                activeDot.classList.remove('active');
            }
            
            // Add active class to clicked dot
            this.classList.add('active');
            
            // Update question number in header
            const questionNumber = this.textContent;
            document.querySelector('.question-number').textContent = questionNumber;
            document.querySelector('.test-progress span:first-child').textContent = `Question ${questionNumber} of 20`;
            
            // Update progress bar
            const progress = (parseInt(questionNumber) / 20) * 100;
            document.querySelector('.progress-bar').style.width = `${progress}%`;
            document.querySelector('.progress-bar').setAttribute('aria-valuenow', progress);
            document.querySelector('.test-progress span:last-child').textContent = `${progress}% Complete`;
        });
    });
    
    // Handle navigation buttons
    const prevButton = document.querySelector('.question-navigation button:first-child');
    const nextButton = document.querySelector('.question-navigation button:last-child');
    
    prevButton.addEventListener('click', function() {
        // Find current active dot
        const activeDot = document.querySelector('.question-dot.active');
        if (activeDot && activeDot.previousElementSibling) {
            // Simulate click on previous dot
            activeDot.previousElementSibling.click();
        }
    });
    
    nextButton.addEventListener('click', function() {
        // Find current active dot
        const activeDot = document.querySelector('.question-dot.active');
        if (activeDot && activeDot.nextElementSibling) {
            // Simulate click on next dot
            activeDot.nextElementSibling.click();
        }
    });
    
    // Handle form submission
    const testForm = document.querySelector('.test-form');
    
    testForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Check if all questions are answered
        const answeredDots = document.querySelectorAll('.question-dot.answered');
        
        if (answeredDots.length < 20) {
            // Show confirmation dialog
            if (confirm(`You have only answered ${answeredDots.length} out of 20 questions. Are you sure you want to submit the test?`)) {
                // Redirect to results page
                window.location.href = '/results';
            }
        } else {
            // Redirect to results page
            window.location.href = '/results';
        }
    });
    
    // Timer functionality
    const timerElement = document.querySelector('.test-timer');
    if (timerElement) {
        const duration = Number.parseInt(timerElement.dataset.duration) || 3600; // Default 1 hour
        let timeLeft = duration;

        const updateTimer = () => {
            const hours = Math.floor(timeLeft / 3600);
            const minutes = Math.floor((timeLeft % 3600) / 60);
            const seconds = timeLeft % 60;

            timerElement.textContent = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

            if (timeLeft <= 300) {
                // 5 minutes left
                timerElement.classList.add("timer-warning");
            }

            if (timeLeft <= 60) {
                // 1 minute left
                timerElement.classList.add("timer-danger");
            }

            if (timeLeft <= 0) {
                clearInterval(timerInterval);

                // Auto-submit the test
                const testForm = document.querySelector(".test-form");
                if (testForm) {
                    const submitEvent = new Event("submit");
                    testForm.dispatchEvent(submitEvent);
                }
            } else {
                timeLeft--;
            }
        }

        updateTimer(); // Initial update
        const timerInterval = setInterval(updateTimer, 1000);
    }
});