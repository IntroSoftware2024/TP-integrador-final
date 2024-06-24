document.querySelector('.close-btn').addEventListener('click', function() {
  window.location.href = "{{ url_for('index') }}";
});
