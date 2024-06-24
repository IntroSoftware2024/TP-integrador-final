document.addEventListener('DOMContentLoaded', function() {
    function openTab(evt, tabName) {

      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }

      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }

      document.getElementById(tabName).style.display = "block";
      evt.currentTarget.className += " active";
    }
  
    document.getElementById('loginTab').addEventListener('click', function(evt) {
      openTab(evt, 'login');
    });
  
    document.getElementById('registerTab').addEventListener('click', function(evt) {
      openTab(evt, 'register');
    });
  
    document.getElementById('loginTab').click();
  });

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