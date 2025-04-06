document.addEventListener("DOMContentLoaded", function () {
    const questions = document.querySelectorAll(".radio-input");

    questions.forEach(question => {
        const options = question.querySelectorAll("input[type='radio']");
        const correctAnswer = question.dataset.correct; // Store correct answer in `data-correct`
        const resultSuccess = question.querySelector(".result.success");
        const resultError = question.querySelector(".result.error");

        options.forEach(option => {
            option.addEventListener("change", function () {
                // Reset classes
                question.classList.remove("correct", "wrong");

                if (this.value === correctAnswer) {
                    question.classList.add("correct");
                    resultSuccess.style.display = "block";
                    resultError.style.display = "none";
                } else {
                    question.classList.add("wrong");
                    resultSuccess.style.display = "none";
                    resultError.style.display = "block";
                }
            });
        });
    });
});
