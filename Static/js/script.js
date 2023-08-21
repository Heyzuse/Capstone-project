document.addEventListener('DOMContentLoaded', function() {
   const yearElement = document.getElementById('footer-year');
   yearElement.textContent = "© " + new Date().getFullYear() + " Your Fitness App";
});

