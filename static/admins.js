function checkAdmin() {
    fetch(`/admins_panel/${userHash}`)
        .then(response => response.json())
        .then(data => {
            // Update the DOM with the user information
            // Replace this code with your own logic
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
