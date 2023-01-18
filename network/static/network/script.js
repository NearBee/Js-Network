document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#likeButton').addEventListener('click', () => {
        like_button();
        console.log("boom");
    });
});

function like_button() {
    // May have to use fetch(), which would require making an mock API request 
    alert("I've been clicked!")
}