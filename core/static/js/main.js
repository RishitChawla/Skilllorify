document.addEventListener("DOMContentLoaded", () => {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
    const navList = document.querySelector(".nav-list")
  
    if (mobileMenuToggle && navList) {
      mobileMenuToggle.addEventListener("click", function () {
        navList.classList.toggle("active")
  
        // Toggle hamburger to X
        const spans = this.querySelectorAll("span")
        if (navList.classList.contains("active")) {
          spans[0].style.transform = "rotate(45deg) translate(5px, 5px)"
          spans[1].style.opacity = "0"
          spans[2].style.transform = "rotate(-45deg) translate(5px, -5px)"
        } else {
          spans[0].style.transform = "none"
          spans[1].style.opacity = "1"
          spans[2].style.transform = "none"
        }
      })
    }
  
    // Close mobile menu when clicking outside
    document.addEventListener("click", (event) => {
      if (
        navList &&
        navList.classList.contains("active") &&
        !event.target.closest(".nav-list") &&
        !event.target.closest(".mobile-menu-toggle")
      ) {
        navList.classList.remove("active")
  
        // Reset hamburger icon
        const spans = mobileMenuToggle.querySelectorAll("span")
        spans[0].style.transform = "none"
        spans[1].style.opacity = "1"
        spans[2].style.transform = "none"
      }
    })
  
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        const targetId = this.getAttribute("href")
        if (targetId === "#") return
  
        const targetElement = document.querySelector(targetId)
        if (targetElement) {
          e.preventDefault()
  
          // Close mobile menu if open
          if (navList && navList.classList.contains("active")) {
            navList.classList.remove("active")
  
            // Reset hamburger icon
            const spans = mobileMenuToggle.querySelectorAll("span")
            spans[0].style.transform = "none"
            spans[1].style.opacity = "1"
            spans[2].style.transform = "none"
          }
  
          window.scrollTo({
            top: targetElement.offsetTop - 80, // Adjust for header height
            behavior: "smooth",
          })
        }
      })
    })
  
    // Animate elements when they come into view
    const animateElements = document.querySelectorAll(".animate-on-scroll")
  
    if (animateElements.length > 0) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("animate-fade-in")
              observer.unobserve(entry.target)
            }
          })
        },
        { threshold: 0.1 },
      )
  
      animateElements.forEach((element) => {
        observer.observe(element)
      })
    }
  
    // Form validation
    const forms = document.querySelectorAll("form")
  
    forms.forEach((form) => {
      form.addEventListener("submit", (e) => {
        let isValid = true
  
        // Get all required inputs
        const requiredInputs = form.querySelectorAll("[required]")
  
        requiredInputs.forEach((input) => {
          // Remove existing error messages
          const existingError = input.parentElement.querySelector(".form-error")
          if (existingError) {
            existingError.remove()
          }
  
          // Check if input is empty
          if (!input.value.trim()) {
            isValid = false
  
            // Create error message
            const errorMessage = document.createElement("div")
            errorMessage.className = "form-error"
            errorMessage.textContent = "This field is required"
  
            // Insert error message after input
            input.parentElement.appendChild(errorMessage)
  
            // Add shake animation
            input.classList.add("shake")
            setTimeout(() => {
              input.classList.remove("shake")
            }, 500)
          }
  
          // Email validation
          if (input.type === "email" && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            if (!emailRegex.test(input.value.trim())) {
              isValid = false
  
              // Create error message
              const errorMessage = document.createElement("div")
              errorMessage.className = "form-error"
              errorMessage.textContent = "Please enter a valid email address"
  
              // Insert error message after input
              input.parentElement.appendChild(errorMessage)
  
              // Add shake animation
              input.classList.add("shake")
              setTimeout(() => {
                input.classList.remove("shake")
              }, 500)
            }
          }
  
          // Password validation
          if (input.type === "password" && input.dataset.minLength && input.value.trim()) {
            const minLength = Number.parseInt(input.dataset.minLength)
            if (input.value.length < minLength) {
              isValid = false
  
              // Create error message
              const errorMessage = document.createElement("div")
              errorMessage.className = "form-error"
              errorMessage.textContent = `Password must be at least ${minLength} characters`
  
              // Insert error message after input
              input.parentElement.appendChild(errorMessage)
  
              // Add shake animation
              input.classList.add("shake")
              setTimeout(() => {
                input.classList.remove("shake")
              }, 500)
            }
          }
        })
  
        // Check password confirmation
        const password = form.querySelector('input[type="password"]')
        const confirmPassword = form.querySelector("input[data-confirm-password]")
  
        if (password && confirmPassword && password.value && confirmPassword.value) {
          if (password.value !== confirmPassword.value) {
            isValid = false
  
            // Create error message
            const errorMessage = document.createElement("div")
            errorMessage.className = "form-error"
            errorMessage.textContent = "Passwords do not match"
  
            // Insert error message after input
            confirmPassword.parentElement.appendChild(errorMessage)
  
            // Add shake animation
            confirmPassword.classList.add("shake")
            setTimeout(() => {
              confirmPassword.classList.remove("shake")
            }, 500)
          }
        }
  
        if (!isValid) {
          e.preventDefault()
  
          // Scroll to first error
          const firstError = form.querySelector(".form-error")
          if (firstError) {
            window.scrollTo({
              top: firstError.offsetTop - 100,
              behavior: "smooth",
            })
          }
        }
      })
    })
  
    // Add keyframe animation for shake
    if (!document.querySelector("#shake-animation")) {
      const style = document.createElement("style")
      style.id = "shake-animation"
      style.textContent = `
              @keyframes shake {
                  0%, 100% { transform: translateX(0); }
                  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                  20%, 40%, 60%, 80% { transform: translateX(5px); }
              }
              .shake {
                  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
              }
          `
      document.head.appendChild(style)
    }
  
    // Initialize tooltips
    const tooltips = document.querySelectorAll("[data-tooltip]")
  
    tooltips.forEach((tooltip) => {
      tooltip.addEventListener("mouseenter", function () {
        const tooltipText = this.getAttribute("data-tooltip")
  
        // Create tooltip element
        const tooltipElement = document.createElement("div")
        tooltipElement.className = "tooltip"
        tooltipElement.textContent = tooltipText
  
        // Position tooltip
        document.body.appendChild(tooltipElement)
  
        const rect = this.getBoundingClientRect()
        tooltipElement.style.top = `${rect.top - tooltipElement.offsetHeight - 10 + window.scrollY}px`
        tooltipElement.style.left = `${rect.left + (rect.width / 2) - tooltipElement.offsetWidth / 2}px`
  
        // Add animation
        setTimeout(() => {
          tooltipElement.style.opacity = "1"
          tooltipElement.style.transform = "translateY(0)"
        }, 10)
  
        // Store tooltip element reference
        this.tooltipElement = tooltipElement
      })
  
      tooltip.addEventListener("mouseleave", function () {
        if (this.tooltipElement) {
          this.tooltipElement.style.opacity = "0"
          this.tooltipElement.style.transform = "translateY(10px)"
  
          setTimeout(() => {
            if (this.tooltipElement && this.tooltipElement.parentNode) {
              this.tooltipElement.parentNode.removeChild(this.tooltipElement)
              this.tooltipElement = null
            }
          }, 300)
        }
      })
    })
  
    // Add tooltip styles
    if (!document.querySelector("#tooltip-styles")) {
      const style = document.createElement("style")
      style.id = "tooltip-styles"
      style.textContent = `
              .tooltip {
                  position: absolute;
                  background-color: rgba(0, 0, 0, 0.8);
                  color: white;
                  padding: 5px 10px;
                  border-radius: 4px;
                  font-size: 12px;
                  z-index: 1000;
                  opacity: 0;
                  transform: translateY(10px);
                  transition: opacity 0.3s, transform 0.3s;
                  pointer-events: none;
              }
              
              .tooltip::after {
                  content: '';
                  position: absolute;
                  top: 100%;
                  left: 50%;
                  margin-left: -5px;
                  border-width: 5px;
                  border-style: solid;
                  border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
              }
          `
      document.head.appendChild(style)
    }
  
    // Google OAuth integration
    const googleButtons = document.querySelectorAll(".google-auth-btn")
  
    googleButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault()
  
        // In a real implementation, this would redirect to Google OAuth
        console.log("Initiating Google OAuth flow")
  
        // For demo purposes, simulate a loading state
        this.classList.add("loading")
        this.disabled = true
  
        const originalText = this.innerHTML
        this.innerHTML = '<span class="spinner"></span> Connecting...'
  
        // Add spinner styles
        if (!document.querySelector("#spinner-styles")) {
          const style = document.createElement("style")
          style.id = "spinner-styles"
          style.textContent = `
                      .spinner {
                          display: inline-block;
                          width: 16px;
                          height: 16px;
                          border: 2px solid rgba(255, 255, 255, 0.3);
                          border-radius: 50%;
                          border-top-color: white;
                          animation: spin 1s ease-in-out infinite;
                          margin-right: 8px;
                      }
                      
                      @keyframes spin {
                          to { transform: rotate(360deg); }
                      }
                  `
          document.head.appendChild(style)
        }
  
        // Simulate OAuth redirect
        setTimeout(() => {
          // Reset button
          this.classList.remove("loading")
          this.disabled = false
          this.innerHTML = originalText
  
          // For demo, show a success message
          const alert = document.createElement("div")
          alert.className = "alert alert-success animate-fade-in"
          alert.innerHTML = "Google authentication successful! Redirecting..."
  
          // Insert alert before the form
          const form = this.closest("form")
          if (form) {
            form.parentNode.insertBefore(alert, form)
          }
  
          // Remove alert after 3 seconds
          setTimeout(() => {
            alert.style.opacity = "0"
            setTimeout(() => {
              if (alert.parentNode) {
                alert.parentNode.removeChild(alert)
              }
            }, 300)
          }, 3000)
        }, 2000)
      })
    })
  
    // Timer functionality for test pages
    const timerElement = document.querySelector(".test-timer")
    if (timerElement) {
      const duration = Number.parseInt(timerElement.dataset.duration) || 3600 // Default 1 hour
      let timeLeft = duration
  
      const updateTimer = () => {
        const hours = Math.floor(timeLeft / 3600)
        const minutes = Math.floor((timeLeft % 3600) / 60)
        const seconds = timeLeft % 60
  
        timerElement.textContent = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
  
        if (timeLeft <= 300) {
          // 5 minutes left
          timerElement.classList.add("timer-warning")
        }
  
        if (timeLeft <= 60) {
          // 1 minute left
          timerElement.classList.add("timer-danger")
        }
  
        if (timeLeft <= 0) {
          clearInterval(timerInterval)
  
          // Auto-submit the test
          const testForm = document.querySelector(".test-form")
          if (testForm) {
            const submitEvent = new Event("submit")
            testForm.dispatchEvent(submitEvent)
          }
        } else {
          timeLeft--
        }
      }
  
      updateTimer() // Initial update
      const timerInterval = setInterval(updateTimer, 1000)
    }
  
    // Certificate animation
    const certificate = document.querySelector(".certificate")
    if (certificate) {
      certificate.addEventListener("mouseenter", function () {
        this.classList.add("certificate-hover")
      })
  
      certificate.addEventListener("mouseleave", function () {
        this.classList.remove("certificate-hover")
      })
  
      // Add certificate hover styles
      if (!document.querySelector("#certificate-styles")) {
        const style = document.createElement("style")
        style.id = "certificate-styles"
        style.textContent = `
                  .certificate {
                      transition: transform 0.5s, box-shadow 0.5s;
                  }
                  
                  .certificate-hover {
                      transform: scale(1.02) rotate(1deg);
                      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                  }
              `
        document.head.appendChild(style)
      }
    }
  
    // OTP input functionality
    const otpInputs = document.querySelectorAll(".otp-input")
  
    if (otpInputs.length > 0) {
      otpInputs.forEach((input, index) => {
        input.addEventListener("input", function () {
          if (this.value.length >= this.maxLength) {
            // Move to next input
            if (index < otpInputs.length - 1) {
              otpInputs[index + 1].focus()
            }
          }
        })
  
        input.addEventListener("keydown", function (e) {
          // On backspace, move to previous input
          if (e.key === "Backspace" && !this.value && index > 0) {
            otpInputs[index - 1].focus()
          }
        })
      })
    }
  })
  
  // Google OAuth callback handler (for demo purposes)
  function handleGoogleCallback() {
    // This would be called after Google OAuth redirect
    console.log("Handling Google OAuth callback")
  
    // For demo purposes, show success message
    const urlParams = new URLSearchParams(window.location.search)
    const success = urlParams.get("success")
  
    if (success === "true") {
      const alert = document.createElement("div")
      alert.className = "alert alert-success animate-fade-in"
      alert.innerHTML = "Google authentication successful! Redirecting to dashboard..."
  
      document.body.insertBefore(alert, document.body.firstChild)
  
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        window.location.href = "/dashboard"
      }, 2000)
    }
  }
  
  // Check if we're on a callback page
  if (window.location.pathname.includes("callback")) {
    handleGoogleCallback()
  }
  