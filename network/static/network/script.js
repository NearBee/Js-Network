document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.likeButton');
    const followButtons = document.querySelectorAll(".followButton");
    const editButtons = document.querySelectorAll(".editButton");
    const submitButtons = document.querySelectorAll(".submitButton");
    const toggleButton = document.querySelector(".modeToggleButton");

    // Get locally saved "body" content to use for setting darkmode (if enabled)
    let body = localStorage.getItem('body');
    document.querySelector("body").classList = body;
    if (body === 'dark-mode') {
        toggleButton.innerHTML = '<i class="bi bi-moon-fill"></i> Dark Mode';
    } else {
        toggleButton.innerHTML = '<i class="bi bi-sun-fill"></i> Light Mode';
    }

    // Finding and utilizing Like Button
    for (let button of likeButtons) {
        button.addEventListener('click', function () {
            let id = button.getAttribute("data-id");
            // let currentLiker = button.getAttribute("request.user")
            like_button(id);
        });
    }

    // Finding and utilizing Follow Button
    for (let button of followButtons) {
        button.addEventListener("click", function () {
            let username = button.getAttribute("data-username");
            follow_button(username);
        });
    }

    // Finding edit buttons
    for (let button of editButtons) {
        button.addEventListener("click", function () {
            let id = button.getAttribute("data-id");
            edit_post(id);
        });
    }

    // Finding Submit buttons
    for (let button of submitButtons) {
        button.addEventListener("click", function () {
            let id = button.getAttribute("data-id");
            submitFunction(id);
        });
    }

    toggleButton.addEventListener("click", function () {
        themeChange();
    })
}
);


function like_button(id, currentLiker) {
    fetch(`/like_post/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            id: id
        })
    })
        .then(() => {
            fetch(`/get_likes/${id}`)
                .then(response => response.json())
                .then(data => {
                    const likes = data.likes;
                    document.querySelector(`#post-${id} .currentLikes`).innerHTML = `Likes: ${likes}`;
                })

                .catch(error => {
                    console.log(`Error: ${error}`);
                });
        })

        .then((response => {
            if (document.querySelector(`#post-${id} .likeButton`).textContent === "Like") {
                document.querySelector(`#post-${id} .likeButton`).innerHTML = `Unlike`;

            } else {
                document.querySelector(`#post-${id} .likeButton`).innerHTML = `Like`;

            }
        }))

        .catch(error => {
            console.log(`Error: ${error}`);
        });
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
                    document.querySelector(".follower_count").innerHTML = `Followers: ${followers}`;
                })

                .catch(error => {
                    console.log(`Error: ${error}`);
                });
        })

        .then((response) => {
            // TODO: also inner html only changing AFTER the first instance rather than reading from page load
            if (document.querySelector(".followButton").textContent === "Follow") {
                document.querySelector(".followButton").innerHTML = `Unfollow`;

            } else {
                document.querySelector(".followButton").innerHTML = `Follow`;
            }
        })

        .catch(error => {
            console.log(`Error:${error}`);
        });
}

function edit_post(id) {
    // Grab and replace the post section with a textarea here
    let editCol = document.querySelector(`#post-${id} .card-text`);
    let editColContent = editCol.textContent;
    let initialRow = document.querySelector(`#post-${id} .card-buttons`);
    let submitRow = document.querySelector(`#post-${id} .submitRow`);

    // Make Changes
    editCol.innerHTML = `<textarea name="post_field" cols="40" rows="10" style="height: 100px; width: 100%; resize: initial;" class="form-control commentField" maxlength="1000" required="">${editColContent}</textarea>`;
    initialRow.style.display = 'none';
    document.querySelector(`#post-${id} .editButton`).style.display = 'none';
    submitRow.style.display = 'flex';

};

function submitFunction(id) {
    // find text area and isolate editedtext
    let editCol = document.querySelector(`#post-${id} .card-text`);
    let textarea = document.querySelector(`#post-${id} textarea[name="post_field"]`);
    let editedText = textarea.value;
    let initialRow = document.querySelector(`#post-${id} .card-buttons`);
    let submitRow = document.querySelector(`#post-${id} .submitRow`);

    // Submit changes presented in edit form here
    fetch(`/submit_edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_field: editedText
        })
    })

        .then((response) => {
            editCol.innerHTML = `<p class="card-text">${editedText}</p>`;
            submitRow.style.display = 'none';
            document.querySelector(`#post-${id} .editButton`).style.display = 'inline-block';
            initialRow.style.display = 'flex';
        })

        .catch(error => {
            console.log(`Error: ${error}`);
        });
}

function themeChange() {
    let button = document.querySelector(".modeToggleButton");
    let element = document.querySelector("body")

    if (!(element.classList.contains('dark-mode'))) {

        // Add darkmode class to change theme based on CSS
        element.classList.add("dark-mode");
        button.innerHTML = '<i class="bi bi-moon-fill"></i> Dark Mode';

        // Change Button color for better readability
        button.classList.remove('btn-outline-dark');
        button.classList.add('btn-outline-light');

        // Save body's class to local storage for a cleaner flow
        localStorage.setItem('body', element.classList);
    } else {

        // Remove darkmode class to change theme based on CSS
        element.classList.remove("dark-mode");
        button.innerHTML = '<i class="bi bi-sun-fill"></i> Light Mode';

        // Change Button color for better readability
        button.classList.remove('btn-outline-light');
        button.classList.add('btn-outline-dark');

        // Save body's class to local storage for a cleaner flow
        localStorage.setItem('body', element.classList);
    }
}