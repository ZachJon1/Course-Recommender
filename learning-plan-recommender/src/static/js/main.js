// This file contains JavaScript code for client-side interactivity, such as form validation and handling user input.

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("learning-plan-form");
    const submitButton = document.getElementById("submit-button");
    const resultContainer = document.getElementById("result-container");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        submitButton.disabled = true;

        const formData = new FormData(form);
        const studentData = {
            academicBackground: formData.get("academicBackground"),
            targetCourse: formData.get("targetCourse")
        };

        fetch("/generate-learning-plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(studentData)
        })
        .then(response => response.json())
        .then(data => {
            resultContainer.innerHTML = `<h3>Recommended Learning Plan:</h3><pre>${data.learningPlan}</pre>`;
        })
        .catch(error => {
            console.error("Error:", error);
            resultContainer.innerHTML = "<p>There was an error generating the learning plan. Please try again.</p>";
        })
        .finally(() => {
            submitButton.disabled = false;
        });
    });
});