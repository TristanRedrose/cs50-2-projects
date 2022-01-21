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
            
            add_post();

            // Clear new post textbox
            document.querySelector('#post-area').value = '';
        }
    })
}

function add_post(){
    
    // Create new post elements
    fetch('/posts/newpost')
    .then(response => response.json())
    .then(post => {

        const newpost = post

        const containerDiv = document.createElement('div');
        containerDiv.setAttribute('id', 'post-div');
        
        containerDiv.innerHTML = `
        <a id="link" href="profile/${newpost.writer}">${newpost.writer}</a>
        <div id="bodytext-div">
            <div id="texty-box">
                <p id="postnum">${newpost.id}</p>
                <p id ="text">${newpost.body}</p>
                <a id = "edit-link" href="#" onclick="event.preventDefault(); get_edit_field(${newpost.id})">Edit</a>
            </div>
        </div>
            <p id="time-text">${newpost.timestamp}</p>
        <div id="like-div">
            <p id="time-text">Likes: ${newpost.likes}</p>
        </div>
        `;

        // Append new post on top of page
        const box = document.querySelector('#post-box');
        box.insertBefore(containerDiv, box.firstChild);

        // Hide last post on page-listing
        boxes = box.querySelectorAll('#post-div');
        boxes[10].style.display = 'none';
    })
}

function get_edit_field (post_id) {
    
    // If any open edits exist close them and restore textbox
    clear_edits(); 
    
    // Show textbox when edit box is removed
    const containerDivs = document.querySelectorAll('#bodytext-div')
    
    containerDivs.forEach(function(containerDiv) {
        if (containerDiv.querySelector('p').innerHTML == post_id) {
            const container = containerDiv;

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