function like (id) {     
    let likes = document.getElementById(`l ${id}`).innerHTML
    fetch('/likes', {
        method: 'POST',
        body: JSON.stringify({
        id: id,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.getElementById(`l ${id}`).innerHTML = parseInt(likes) + 1;
        document.getElementById(`like ${id}`).style.display = 'none';
        document.getElementById(`unlike ${id}`).style.display = 'block';
    })      
}

function unlike (id) {   
    let likes = document.getElementById(`l ${id}`).innerHTML
    fetch('/unlike', {
        method: 'POST',
        body: JSON.stringify({
        id: id,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);        
        document.getElementById(`l ${id}`).innerHTML = parseInt(likes) - 1;
        document.getElementById(`unlike ${id}`).style.display = 'none';
        document.getElementById(`like ${id}`).style.display = 'block';
    })    
}
