var csrfToken = Cookies.get('csrftoken');
var createGradeForm = document.querySelector('#create_grade_form');
var deleteGradeForm = document.querySelector('#delete_grade_form');
var updateGradeForm = document.querySelector('#update_grade_form');
var currentGradeText = document.querySelector('#current_grade_text');
var gradeForms = document.querySelector('#grade_forms');
var averageGradeText = document.querySelector('#average_grade_text');
var gradeSlider = document.querySelector('#grade_slider');
var grade;

const GRADE_WIDTH = 20;

if(createGradeForm) {
	createGradeForm.onsubmit = function(e) {
		e.preventDefault();
		var form = createGradeForm;
		if(isNaN(grade)) return;
		form.value.value = grade;
		var gradeData = new FormData(form);
		var xhr = new XMLHttpRequest();
		xhr.open('post', form.action);
		xhr.setRequestHeader('X-CSRFToken', csrfToken);
		xhr.send(gradeData);
		xhr.onreadystatechange = function() {
			if(xhr.readyState == 4) {
				if(xhr.status == 201) {
					switchUpdateMode(xhr);
				}
			}
		}
	}
}

if(updateGradeForm) {
	updateGradeForm.onsubmit = function(e) {
		e.preventDefault();
		var form = updateGradeForm;
		if(isNaN(grade)) return;
		form.value.value = grade;
		var gradeData = new FormData(form);
		var xhr = new XMLHttpRequest();
		xhr.open('put', form.action);
		xhr.setRequestHeader('X-CSRFToken', csrfToken);
		xhr.send(gradeData);
		xhr.onreadystatechange = function() {
			if(xhr.readyState == 4) {
				if(xhr.status == 201) {
					switchUpdateMode(xhr);
				}
			}
		}
	}
}

if(deleteGradeForm) {
	deleteGradeForm.onsubmit = function(e) {
		e.preventDefault();
		var form = deleteGradeForm;
		var xhr = new XMLHttpRequest();
		xhr.open('delete', form.action);
		xhr.setRequestHeader('X-CSRFToken', csrfToken);
		xhr.send();
		xhr.onreadystatechange = function() {
			if(xhr.readyState == 4) {
				if (xhr.status == 204) {
					switchCreateMode();
				}
			}
		}
	}
}

gradeSlider.onclick = function(e) {
	var coords = getCoords(gradeSlider);
	grade = (parseFloat(e.clientX) - coords.left) /
		parseFloat(getComputedStyle(gradeSlider).width) * 10;
	grade = Math.ceil(grade);
	let stars = document.createElement('div');
	gradeSlider.innerHTML = '';
	gradeSlider.appendChild(stars);
	stars.classList.add('grade-stars');
	stars.style.width = grade * GRADE_WIDTH + 'px';
}



function switchCreateMode() {
	gradeSlider.innerHTML = '';
	currentGradeText.innerHTML = '';
	updateGradeForm.value.value = '';
	createGradeForm.value.value = '';
	createGradeForm.classList.remove('d-none');
	updateGradeForm.classList.add('d-none');
	deleteGradeForm.classList.add('d-none');
	getAverageGrade(getBookId(), averageGradeText);
}

function switchUpdateMode(xhr) {
	updateGradeForm.value.value = '';
	createGradeForm.value.value = '';	
	currentGradeText.innerHTML = 'Ваша оценка - ' 
		+ xhr.responseText;
	createGradeForm.classList.add('d-none');
	updateGradeForm.classList.remove('d-none');
	deleteGradeForm.classList.remove('d-none');
	getAverageGrade(getBookId(), averageGradeText);
}

function getAverageGrade(bookId, averageGradeBox) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', `/api/book/${bookId}/`);
	xhr.send();
	xhr.onreadystatechange = function() {
		if(xhr.readyState == 4) {
			if(xhr.status == 200) {
				var bookData = JSON.parse(xhr.responseText);
				if(bookData.average_grade != 'False') {
					averageGradeBox.innerHTML ='Средняя оценка пользователей: ' +
					bookData.average_grade;
				}
				else {
					averageGradeBox.innerHTML = 'Оценок еще нет ...';
				}
				
			}
		}
	}
}

function getBookId() {
	var absoluteUrl = window.location.href;
	var result = absoluteUrl.match(/catalog\/book\/(\d+)\//);
	return result[1];
}

function getCoords(elem) {
  let box = elem.getBoundingClientRect();

  return {
    top: box.top + pageYOffset,
    left: box.left + pageXOffset
  }
}