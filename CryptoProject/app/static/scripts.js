// This function executes when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to the send message form
    document.getElementById('sendMessageForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent form submission
        let message = document.getElementById('message').value;
        let to_number = document.getElementById('to_number').value;
        
        // Make a POST request to send the message
        let response = await fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, to_number })
        });

        // Handle the response
        let result = await response.json();
        alert(result.status ? 'Message sent successfully!' : 'Failed to send message.');
    });

    // Add event listener to the receive message form
    document.getElementById('receiveMessageForm').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent form submission
        let otp = document.getElementById('otp').value;
        let message_id = document.getElementById('message_id').value;
        
        // Make a POST request to decrypt the message
        let response = await fetch('/receive_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ otp, message_id })
        });

        // Handle the response
        let result = await response.json();
        alert(result.message ? `Decrypted Message: ${result.message}` : 'Failed to decrypt message.');
    });
});
