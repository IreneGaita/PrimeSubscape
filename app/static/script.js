// Funzione per aggiornare l'altezza del background-blur
function updateBackgroundBlurHeight() {
    var pageHeight = document.documentElement.scrollHeight;
    var backgroundBlur = document.getElementById('background-blur');
    backgroundBlur.style.height = pageHeight + 'px';
}
        
        // Aggiorna l'altezza del background-blur al caricamento della pagina
window.onload = updateBackgroundBlurHeight;
        
        // Aggiorna l'altezza del background-blur quando la finestra viene ridimensionata
window.onresize = updateBackgroundBlurHeight;

function deleteFunction(userId){
        //call localhost:5000/deleteUser
        fetch('http://localhost:5000/delete_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userId: userId}),
        })
        //reload the page
        .then(() => {
                //elimina l'elemento con l'id specificato
                document.getElementById(userId).remove();
        })
        
}

function editFunction(userId){
        //go to the page to edit the user
        window.location.href = 'http://localhost:5000/edit_user/' + userId;
}