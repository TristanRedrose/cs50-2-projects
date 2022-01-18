document.addEventListener('DOMContentLoaded', function() {

    load_posts('all');

    // Use submit button to make post
    const postForm = document.querySelector('#post-form')

    // If form exists add event listener
    if (postForm !== null) {
        postForm.addEventListener('submit', function(event) {
            event.preventDefault();
            make_post();
        });
    }
})

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
            clear('#posts-box');
            load_posts('all');

            // Clear new post textbox
            document.querySelector('#post-area').value = '';
        }
    });
}

function load_posts(writer) {
    
    // Get name of current user
    const user_name = JSON.parse(document.getElementById('user_name').textContent);

    fetch(`/posts/${writer}`)
    .then(response => response.json())
    .then(posts => {
        //print posts
        console.log(posts);

        const allposts = posts
        
        // Create html elements for each post
        allposts.forEach(post => {
            
            // Create main container
            const mainDiv = document.createElement('div');
            mainDiv.setAttribute('id', 'post-div');
            
            // Make link to writers profile page
            const writerName = document.createElement('a');
            writerName.setAttribute('href', `profile/${post.writer}`);
            writerName.setAttribute('id', 'link');
            writerName.innerText =`${post.writer}`;
            mainDiv.appendChild(writerName);
            
            // Create body div
            const bodyDiv = document.createElement('div');
            bodyDiv.setAttribute('id', 'bodytext-div');
            
            // Create body-text and edit link div
            const textDiv = document.createElement('div');
            textDiv.setAttribute('id', 'texty-div');

            // Add an edit option if the current user is also the post writer
            if (user_name === post.writer) {

                const editLink = document.createElement('a');
                editLink.setAttribute('href', '#');
                editLink.setAttribute('id', 'edit-link');
                editLink.innerText = 'Edit';
                textDiv.appendChild(editLink);
                
                // Add edit link functionality
                editLink.addEventListener('click', function(event) {
                    event.preventDefault();
        
                    // Remove any open edit boxes when a new one is opened
                    if (document.querySelector('#edit-div') != null) {
                        const editDivs = document.querySelectorAll('#edit-div')
                    
                        editDivs.forEach(function(editDiv) {
                            editDiv.remove();
                        })
                    }
                    
                    // Show textbox when edit box is removed
                    const textDivs = document.querySelectorAll('#texty-div')
                    
                    textDivs.forEach(function(textDiv) {
                        if (textDiv.style.display == 'none') {
                            textDiv.style.display = 'block';
                        }
                    })
                    
                    // Hide current text
                    textDiv.style.display= 'none';
                    
                    // Display edit field
                    get_edit_field(`${post.body}`, textDiv, bodyDiv, `${post.id}`);
                })
            }

            // Add post bodytext
            const bodyText = document.createElement('p');
            bodyText.innerText =`${post.body}`;
            textDiv.appendChild(bodyText);
            
            // Add text and edit link to main body div
            bodyDiv.appendChild(textDiv);
            
            // Add body div to main post div
            mainDiv.appendChild(bodyDiv);
            
            // Add timestamp
            const time = document.createElement('p');
            time.setAttribute('id', 'time-text');
            time.innerText =`${post.timestamp}`;
            mainDiv.appendChild(time);
            
            // Make div for likes and like button
            const likeDiv = document.createElement('div');
            likeDiv.setAttribute('id', 'like-div');

            // Add like count
            const likes = document.createElement('p');
            likes.setAttribute('id', 'time-text');
            likes.innerText =`Likes: ${post.likes}`;
            likeDiv.appendChild(likes);
            
            // Add like button if user is not also the writer
            if (user_name !== post.writer) {

                // Create link and button-image
                const likeImage = document.createElement('img');
                likeImage.setAttribute('src','https://www.vectorico.com/wp-content/uploads/2018/02/Like-Icon.png');
                likeImage.setAttribute('id', 'like-img');
            
                // Wrap link around the button image
                const likeLink = document.createElement('a');
                likeLink.setAttribute('href', `posts/${post.id}`);
                likeLink.setAttribute('id', 'like-link');
                likeLink.appendChild(likeImage);
                
                // If user not authorised, prompt for a login
                if (user_name === '') {
                    likeLink.setAttribute('href', '/login');
                }
            
                likeDiv.appendChild(likeLink);
            }
            
            // Add like count div to main post container
            mainDiv.appendChild(likeDiv);

            //Append post to page
            document.querySelector("#posts-box").append(mainDiv);  
        });
    })
}

function clear(element) {
    
    // Clear div 
    var div = document.querySelector(element);
    while(div.firstChild) {
        div.removeChild(div.firstChild);
    }
}

function get_edit_field (bodyText, text_container, main_container, post_id) {

    // Create container for edit elements
    const editDiv= document.createElement('div');
    editDiv.setAttribute('id', 'edit-div');

    // Create form elements 
    const form = document.createElement('form');
    form.setAttribute('class', 'edit-form');

    const textArea = document.createElement('textarea');
    textArea.innerText = bodyText;
    textArea.setAttribute('id', 'edit-area');
    form.appendChild(textArea);

    const submitButton = document.createElement('input');
    submitButton.setAttribute('type', 'submit');
    submitButton.setAttribute('id', 'edit-submit');
    form.appendChild(submitButton);

    // Add edit form functionality
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        edit_post(post_id);
    })

    const cancelButton = document.createElement('button');
    cancelButton.setAttribute('id', 'edit-submit');
    cancelButton.style.marginLeft = '10px';
    cancelButton.innerText = 'Cancel';
    form.appendChild(cancelButton);

   
    // Add cancel button functionality
    cancelButton.addEventListener('click', function(event) {
        event.preventDefault();
        editDiv.remove();
        text_container.style.display = 'block';
    })
    
    // Append form elements to edit container
    editDiv.appendChild(form);

    // Append edit container to main container
    main_container.appendChild(editDiv);
}

function edit_post(post_id) {
  
    // Make post
    fetch(`/posts/edit/${post_id}`, {
      method: 'POST',
      body: JSON.stringify({
          body: document.querySelector('#edit-area').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        
        // Clear previous post list if it exists, and re-list posts
        if (result.message === 'Post edited.') {
            clear('#posts-box');
            load_posts('all');
        }
    });
}

