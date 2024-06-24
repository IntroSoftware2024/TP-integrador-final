document.addEventListener('DOMContentLoaded', function() {
    console.log('login.js loaded');
    var mensajeError = document.getElementById('mensajeError');
    
    if (mensajeError) {
      var windowHeight = window.innerHeight; 
      var mensajeErrorTop = mensajeError.getBoundingClientRect().top;
      var offset = mensajeErrorTop - (windowHeight / 2); 

      window.scrollBy({ top: offset, behavior: 'smooth' });
    }
  });