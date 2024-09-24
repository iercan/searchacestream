function show_message(text){
    const div = document.getElementById('submit_message_div');
    const message_span = document.getElementById('submit_message');
    div.style.display = 'flex';
    message_span.innerHTML = text;
    setTimeout(() => {
        div.style.display = 'none';
    }, 1500);


}

document.getElementById('submitForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const contentId = document.getElementById('contentId').value;
    const keywords = document.getElementById('keywords').value;

    // Create a data object to send with the POST request
    const data = {
        contentId: contentId,
        keywords: keywords
    };

    // Send a POST request using fetch
    fetch('/submit_content_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            show_message(data.message);

        })
        .catch((error) => {
            console.error('Error:', error);
            show_message("There is an error!")
            // Handle errors here, such as displaying an error message to the user
        });
});
