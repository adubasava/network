// If edit button is clicked, edit the post
document.addEventListener('click', event => {

    // Find what was clicked on
    const element = event.target;

    if (element.className === 'editbtn') {     
        document.getElementById(`${element.parentElement.id}`).style.display = 'none';  
        document.getElementById(`${element.parentElement.id.split(" ")[1]}`).style.display = 'block';
    }

    // If save button is clicked, save the post
    if (element.className === 'save') {
        document.getElementById(`${element.parentElement.id}`).style.display = 'block';  
        element.parentElement.style.display = 'none';
        let content = document.getElementById(`t ${element.parentElement.id}`).value

        fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({
            id: element.parentElement.id,
            content: content,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.getElementById(`edit ${element.parentElement.id}`).style.display = 'block';  
            document.getElementById(`s ${element.parentElement.id}`).innerHTML = content;
            console.log(document.getElementById(`s ${element.parentElement.id}`).innerHTML)            
        })        
    }   
});
