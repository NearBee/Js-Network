document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('#likeButton');
    const followButtons = document.querySelectorAll("#followButton");

    for (let button of likeButtons) {
        button.addEventListener('click', like_button);
    }
    if (followButtons) {
        console.log("follow button found");
        for (let button of followButtons) {
            button.addEventListener("click", function () {
                let username = button.getAttribute("data-username");
                follow_button(username);
            });
        }
    } else {
        console.log("follow button not found");
    }
});


function like_button() {
    alert("I've been clicked!");
}

function follow_button(username) {

    fetch(`/follow_unfollow/${username}`, {
        method: 'POST',
        body: JSON.stringify({
            username: username
        })
    })
        .then(() => {
            fetch(`/get_followers/${username}`)
                .then(response => response.json())
                .then(data => {
                    const followers = data.followers;
                    document.querySelector("#follower_count").innerHTML = `Followers: ${followers}`;
                })
                .catch(error => {
                    console.log(`Error: ${error}`);
                })
        })
        .then((response) => {
            if (document.querySelector("#followButton").contains("Follow")) {
                // TODO: Doesn't currently work fix this so that the innerHTML
                document.querySelector("#followButton").innerHTML = `<button class="followButton" data-username="${username}">Unfollow</button>`;
            } else {
                document.querySelector("#followButton").innerHTML = `<button class="followButton" data-username="${username}">Follow</button>`;
            }
        })
        .catch(error => {
            console.log(`Error:${error}`);
        });
}


// May have to use fetch(), which would require making an mock API request
// Look at Lecture 5 notes "Counter" for an idea of what to possibly do
// Maybe do something like "likes++" if button === "like"