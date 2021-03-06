var form = document.querySelector('#add_book_form');
var csrfToken = Cookies.get('csrftoken');

form.onsubmit = function(e) {
	e.preventDefault();
	bookData = new FormData(form);

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/api/books/');
	// xhr.setRequestHeader('Content-Type', 'multipart/form-data');
	xhr.setRequestHeader('X-CSRFToken', csrfToken);
	xhr.send(bookData);
	xhr.onreadystatechange = function() {
		if(xhr.readyState == 4) {
			if(xhr.status == 201) form.reset();
			var message = createMessage(xhr);
			document.body.appendChild(message);
		}
	}
}

function createMessage(xhr) {
	var message = document.createElement('p');


	var message = document.createElement('p');
		message.classList.add('fixed-top', 'w-25',
	    'alert');
	
	if(xhr.status == 201) {
		bookAdded = JSON.parse(xhr.responseText);
		message.classList.add('alert-success');
		message.innerHTML = `Книга "${bookAdded.title}", 
		успешно добавлена, 
		перезагрузите страницу, чтобы увидеть ее в списке`;
	}
	else if(xhr.status == 400) {
		message.classList.add('alert-danger');
		message.innerHTML = `${xhr.responseText}`;
	}
	else if(xhr.status == 403) {
		message.classList.add('alert-danger');
		message.innerHTML = `${xhr.responseText}`
	}
	else {
		message.classList.add('alert-info');
		message.innerHTML = 'Что то пошло не так';
	}

	var closer = document.createElement('span');
	closer.classList.add('closer');
	closer.innerHTML = "&#9746;"
	message.appendChild(closer);

	closer.onclick = function() {
		document.body.removeChild(message);
	}

	return message;
}