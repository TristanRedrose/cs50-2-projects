function make_post() {
    
    // Make post
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-area').value
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        
        // Clear previous post list if it exists, and re-list posts
        if (result.message === 'Post submitted.') {
            
            location.reload();
        }
    })
}

function get_edit_field (post_id) {
    
    // If any open edits exist close them and restore textbox
    clear_edits();
    
    // Find current selected post
    const allPosts = document.querySelectorAll('#post-div')
    allPosts.forEach(function(post) {
        if (post.querySelector("#postnum").innerHTML == post_id) {
            const container = post.querySelector('#bodytext-div');

            const text = container.querySelector('#text').innerText;

            // Hide current post bodytext
            container.querySelector('#texty-box').style.display = 'none';
            
            // Create container for edit elements
            const editDiv = document.createElement('div');
            editDiv.setAttribute('id', 'edit-div');
            
            editDiv.innerHTML = `
            <form class="edit-form">
                <textarea id="edit-area">${ text }</textarea>
                <input type="submit" id="edit-submit" onclick="event.preventDefault(); edit_post(${post_id})">
                <button id="edit-submit" style="margin-left: 10px" onclick="event.preventDefault(); clear_edits()">Cancel</button>
            </form> 
            `;

            // Append edit container to main container
            container.appendChild(editDiv);
        }
    })
}

function edit_post(post_id) {

    const text = document.querySelector('#edit-area').value;
    // Make post
    fetch(`/posts/edit/${post_id}`, {
      method: 'POST',
      body: JSON.stringify({
          body: text
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        
        // If edit succesfull, remove edit div and show changed post
        if (result.message === 'Post edited.') {
            const textDivs = document.querySelectorAll('#texty-box');
                    
            textDivs.forEach(function(textDiv) {
                if (textDiv.style.display == 'none') {
                    document.querySelector('#edit-div').remove();
                    textDiv.querySelector('#text').innerText = text;
                    textDiv.style.display = 'block';
                }
            })
        }
    })
}

function clear_edits() {
     
    // Remove any open edit boxes when a new one is opened
    if (document.querySelector('#edit-div') != null) {
        const editDivs = document.querySelectorAll('#edit-div');

        editDivs.forEach(function(editDiv) {
            editDiv.remove();
        })
    }

    // Show textbox when edit box is removed
    const textyDivs = document.querySelectorAll('#texty-box')
    
    textyDivs.forEach(function(textDiv) {
        if (textDiv.style.display == 'none') {
            textDiv.style.display = 'block';
        }
    })
}

function follow_unfollow(profile_name) {

    fetch(`/posts/follows/${profile_name}`)
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result)

        const value = document.querySelector('#count').innerText
        let count = parseInt(value, 10)

        // Update follower count
        if (result.message === `Following ${profile_name}.`) {
            count = count + 1;
            document.querySelector('#count').innerText = count;
            document.querySelector('#follow-button').innerText = 'Unfollow';
        }

        if (result.message === `Unfollowed ${profile_name}.`) {
            count = count - 1;
            document.querySelector('#count').innerText = count;
            document.querySelector('#follow-button').innerText = 'Follow';
        }
    })
}

function like_unlike(post_id) {

    fetch(`/posts/likes/${post_id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result)

        const allPosts = document.querySelectorAll('#post-div')

        allPosts.forEach(function(post) {
            if (post.querySelector("#postnum").innerHTML == post_id) {
                const image = post.querySelector('#like-img');
                
                const value = post.querySelector('#like-num').innerHTML
                let count = parseInt(value)

                // Update count and thumbs-img
                if (result.message === "Post liked.") {
                    count = count + 1
                    post.querySelector('#like-num').innerHTML = count
                    image.setAttribute('src','https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Not_facebook_not_like_thumbs_down.png/1196px-Not_facebook_not_like_thumbs_down.png');
                    image.setAttribute('alt', 'thumbsdown');
                }

                if (result.message === "Post unliked.") {
                    count = count - 1
                    post.querySelector('#like-num').innerHTML = count
                    image.setAttribute('src','https://www.vectorico.com/wp-content/uploads/2018/02/Like-Icon.png');
                    image.setAttribute('alt', 'thumbsup');
                }
            }
        })
    })
}
