function loadUserInfo(userHash) {
    fetch(`/api/user/${userHash}`)
        .then(response => response.json())
        .then(data => {
            // Update the DOM with the user information
            // Replace this code with your own logic
            document.getElementsByClassName("user-info")[0].textContent = data.email
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
