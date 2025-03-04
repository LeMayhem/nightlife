document.addEventListener('DOMContentLoaded', (event) => {
    const input = document.getElementById('search_artist');
    if (input) {
      input.addEventListener('keyup', (e) => {
        var inputs = e.target.value.toLowerCase(); //do lowercase
        //loop through outer div and hide it
        document.querySelectorAll( '.first-letter, .artist-card').forEach(function(el) {
          el.style.display = 'none';
        });
        //loop through outer ->card-title
        document.querySelectorAll('.artist-card .name h5').forEach(function(el) {
          //compare 
          if (el.textContent.toLowerCase().indexOf(inputs) > -1) {
            el.closest('.artist-card').style.display = "block"; //if match show that div
          }
        });
      });
    } else {
      console.error("Element with ID 'search_artist' not found.");
    }
  });