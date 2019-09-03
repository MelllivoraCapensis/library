var form = document.querySelector('#add_author_form');
var csrfToken = Cookies.get('csrftoken');

form.onsubmit = function(e) {
	e.preventDefault();
	// authorData = JSON.stringify({
	// 	'first_name': form.first_name.value,
	// 	'last_name': form.last_name.value,
	// 	'date_of_birth': form.date_of_birth.value,
	// 	'date_of_death': form.date_of_death.value,
	// 	'biography': form.biography.value,
	// });
	var authorData = new FormData(form);
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/api/authors/');
	// xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('X-CSRFToken', csrfToken);
	xhr.send(authorData);
	xhr.onreadystatechange = function() {
		if(xhr.readyState == 4) {
			console.log(xhr);
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
		authorAdded = JSON.parse(xhr.responseText);
		message.classList.add('alert-success');
		message.innerHTML = `Автор ${authorAdded.last_name}, 
		${authorAdded.first_name} успешно добавлен, 
		перезагрузите страницу, чтобы увидеть его в списке`;
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