document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Use submit button to send mail
  document.querySelector('#compose-form').addEventListener('submit', function(event) {
    event.preventDefault();
    send_email();
  });

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    
    const mail = emails

    mail.forEach(email => {
       
      const mainDiv = document.createElement('div');
      mainDiv.setAttribute('id', 'main-container');

      // Create link wrapper
      const link = document.createElement('a');
      link.setAttribute('href', '');
      link.setAttribute('id', 'link');

      // Create mail container
      const contDiv = document.createElement('div');
      contDiv.setAttribute('id', 'container');
      
      // Create content and append it to container
      const senderDiv = document.createElement('div');
      senderDiv.setAttribute('id', 'sender');
      senderDiv.innerText =`${email.sender}`;
      contDiv.appendChild(senderDiv);

      const subjectDiv = document.createElement('div');
      subjectDiv.setAttribute('id', 'subject');
      subjectDiv.innerText = `${email.subject}`;
      contDiv.appendChild(subjectDiv);

      const timeDiv = document.createElement('div');
      timeDiv.setAttribute('id', 'time');
      timeDiv.innerText = `${email.timestamp}`;
      contDiv.appendChild(timeDiv);

      const buttonDiv = document.createElement('div');
      buttonDiv.setAttribute('id', 'button-container');
      
      // Dont show archive button in sent mail
      if (mailbox !== 'sent') {
        const archButton = document.createElement('button');
        archButton.setAttribute('id', 'archive');

        // Set button function depending on mailbox view
        if (mailbox === 'inbox') {
          archButton.innerText = 'Archive';
          archButton.addEventListener('click', () => archive(email.id, true));
        }
        else {
          archButton.innerText = 'Unarchive';
          archButton.addEventListener('click', () => archive(email.id, false));
        }
        buttonDiv.appendChild(archButton);
      }
      
      // Wrap link around container
      link.appendChild(contDiv);

      // Add everything to main container
      mainDiv.append(link);
      mainDiv.append(buttonDiv);
      
      // Set grey background if message is read
      if (email.read === true) {
        contDiv.style.backgroundColor = 'lightgrey';
      }
      else {
        contDiv.style.backgroundColor = 'white';
      }
      
      // Add mail to html
      document.querySelector('#emails-view').append(mainDiv);
      
      // Add detailed view function to item in mailbox
      link.addEventListener('click', function(event) {
        event.preventDefault()
        mail_view(email.id)
      })
    });
  });
}

function send_email() {
  
  // Send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);

      // If message sent load sent messages, else raise alert
      if (result.message === 'Email sent successfully.') {
        load_mailbox('sent');
      }
      else {
        alert(result.error);
      }
  });
}

function mail_view(mail_id) {

  // Clear pre-existing html
  document.querySelector('#mail-view').innerHTML = '';

  // Show mail view and hide other views
  document.querySelector('#mail-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Get email info
  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    const mail = email
    
    // Create mail container
    const infoContainer = document.createElement('div');
    
    // Create content and append it to container
    const fromDiv = document.createElement('div');
    fromDiv.innerHTML =`<b>From:</b> ${mail.sender}`;
    infoContainer.appendChild(fromDiv);

    const toDiv = document.createElement('div');
    toDiv.innerHTML =`<b>To:</b> ${mail.recipients}`;
    infoContainer.appendChild(toDiv);

    const subjectDiv = document.createElement('div');
    subjectDiv.innerHTML =`<b>Subject:</b> ${mail.subject}`;
    infoContainer.appendChild(subjectDiv);

    const timeDiv = document.createElement('div');
    timeDiv.innerHTML =`<b>Timestamp:</b> ${mail.timestamp}`;
    infoContainer.appendChild(timeDiv);

    const replyButton = document.createElement('button');
    replyButton.setAttribute('class', 'btn btn-sm btn-outline-primary');
    replyButton.innerText = 'Reply';
    infoContainer.appendChild(replyButton);
    
    const hr = document.createElement('hr');
    infoContainer.appendChild(hr);

    const bodyDiv = document.createElement('div');
    bodyDiv.innerText =`${mail.body}`;
    infoContainer.appendChild(bodyDiv);


    document.querySelector('#mail-view').append(infoContainer);
    
    // Add reply functionality to button
    replyButton.addEventListener('click', () => reply(mail));
    
    // Mark email as read
    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  });
}

function reply(mail) {
  
  // Show empty compose form
  compose_email();
  
  // Prefill form with existing data
  document.querySelector('#compose-recipients').value = `${mail.sender}`;
  if ((mail.subject).substring(0, 3) === 'Re:') {
    document.querySelector('#compose-subject').value = `${mail.subject}`;
  }
  else {
    const subject = `Re: ${mail.subject}`;
    document.querySelector('#compose-subject').value = subject;
  }
  document.querySelector('#compose-body').value = `On ${mail.timestamp} ${mail.sender} wrote: \n${mail.body}`;
}

function archive(mail_id, bool) {
  fetch(`/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: bool
    })
  })
  .then(() => load_mailbox('inbox'));
}

