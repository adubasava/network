document.addEventListener('DOMContentLoaded', function() {    
  
    // Waiting for the click on submit button
    document.querySelector('#create-post').addEventListener('submit', new_post);
    
})
    
function new_post () {    
  fetch('/posts', {
    method: 'POST',
    body: JSON.stringify({
    content: document.querySelector('#create').value,
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
  })    
}




