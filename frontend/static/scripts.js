document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addCourseButton').addEventListener('click', function() {
        const coursesContainer = document.getElementById('coursesContainer');
        const newCourseEntry = document.createElement('div');
        newCourseEntry.classList.add('courseEntry');
        newCourseEntry.innerHTML = `
            <label for="subject">Materia:</label>
            <input type="text" class="subject" name="subject" required>
            
            <label for="career">Carrera:</label>
            <input type="text" class="career" name="career" required>
            
            <label for="enrollmentYear">Año de Inscripción:</label>
            <input type="number" class="enrollmentYear" name="enrollmentYear" required>
            
            <label for="timesTaken">Número de Veces Cursada:</label>
            <input type="number" class="timesTaken" name="timesTaken" required>
        `;
        coursesContainer.appendChild(newCourseEntry);
    });
});

document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const courseEntries = document.querySelectorAll('.courseEntry');
    const courses = Array.from(courseEntries).map(entry => ({
        subject: entry.querySelector('.subject').value,
        career: entry.querySelector('.career').value,
        year_of_enrollment: parseInt(entry.querySelector('.enrollmentYear').value),
        times_taken: parseInt(entry.querySelector('.timesTaken').value)
    }));

    const formData = {
        full_name: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        address: document.getElementById('address').value,
        phone: document.getElementById('phone').value,
        registration_date: new Date().toISOString(),
        courses: courses
    };

    fetch('http://localhost:8000/api/leads/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    }).then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error('Error en la solicitud: ' + err.message);
            });
        }
        return response.json();
    }).then(data => {
        const confirmationMessage = document.getElementById('confirmationMessage');
        confirmationMessage.classList.remove('hidden');
        confirmationMessage.textContent = `Registro exitoso. ID del registro: ${data.id}`;
    }).catch(error => {
        const confirmationMessage = document.getElementById('confirmationMessage');
        confirmationMessage.classList.remove('hidden');
        confirmationMessage.textContent = `Error: ${error.message}`;
        console.error('Error:', error);
    });
});