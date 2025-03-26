function validatePassword() {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;
    let errorMessage = document.getElementById("error-message");

    if (password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match!";
        return false; // Prevent form submission
    }

    errorMessage.textContent = ""; // Clear error message if passwords match
    return true; // Allow form submission
}