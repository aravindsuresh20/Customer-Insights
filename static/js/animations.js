// Update the heading animation code
document.addEventListener('DOMContentLoaded', function() {
    const heading = document.querySelector('.animated-heading');
    const text = heading.getAttribute('data-text');
    
    // Clear existing content
    heading.innerHTML = '';
    
    // Create animated letters
    for (let i = 0; i < text.length; i++) {
      const letter = document.createElement('span');
      letter.className = 'letter';
      letter.textContent = text[i];
      letter.style.animationDelay = `${i * 0.1}s`;
      heading.appendChild(letter);
      
      // Add space for space characters
      if (text[i] === ' ') {
        letter.style.padding = '0 0.2rem';
      }
    }
  });
  
    // Add floating animation to form inputs on focus
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-5px)';
      });
      
      input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
      });
    });
  
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
      button.addEventListener('click', function(e) {
        const x = e.clientX - e.target.getBoundingClientRect().left;
        const y = e.clientY - e.target.getBoundingClientRect().top;
        
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        this.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 1000);
      });
    });
  
    // Add parallax effect to background
    document.addEventListener('mousemove', function(e) {
      const bg = document.querySelector('.animated-bg');
      const x = e.clientX / window.innerWidth;
      const y = e.clientY / window.innerHeight;
      
      bg.style.transform = `translate(-${x * 20}px, -${y * 20}px)`;
    });
  
    // Add scroll animation to elements
    const observerOptions = {
      threshold: 0.1
    };
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate__animated', 'animate__fadeInUp');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);
  
    document.querySelectorAll('.glass-card, .result-card').forEach(card => {
      observer.observe(card);
    });

  
  // Form submission animation
  document.getElementById('loanForm')?.addEventListener('submit', function(e) {
    const submitBtn = this.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
      submitBtn.disabled = true;
    }
  });