document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('#likeButton');
    for (let button of likeButtons) {
        button.addEventListener('click', like_button);
    }
});

function like_button() {
    alert("I've been clicked!")
}
// May have to use fetch(), which would require making an mock API request 