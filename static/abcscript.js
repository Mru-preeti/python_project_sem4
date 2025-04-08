function validatePassword(event) {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;
    let errorMessage = document.getElementById("error-message");
    console.log("Validation triggered");

    // Check password strength
    let error = checkPassword(password);
    if (error) {
        errorMessage.textContent = error; // Show error below input field
        return false; // Prevent form submission
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match!";
        return false; // Prevent form submission
    }

    errorMessage.textContent = ""; // Clear error if everything is correct
    alert("Sign in Successful!");
    window.location.href = "Main.html"; // Redirect to main page
    return false; // Prevent default form submission
}

// Function to check password strength
function checkPassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (password.length < minLength) {
        return "Password must be at least 8 characters long, contain at least one uppercase letter, at least one number, and at least one special character.";
    }
    if (!hasUpperCase) {
        return "Password must be at least 8 characters long, contain at least one uppercase letter, at least one number, and at least one special character.";
    }
    if (!hasNumber) {
        return "Password must be at least 8 characters long, contain at least one uppercase letter, at least one number, and at least one special character.";
    }
    if (!hasSpecialChar) {
        return "Password must be at least 8 characters long, contain at least one uppercase letter, at least one number, and at least one special character.";
    }
    return null; // Password is valid
}

// Attach validation to form submit event
document.getElementById("signupForm").addEventListener("submit", function(event) {
    if (!validatePassword(event)) {
        event.preventDefault(); // Stop form submission if validation fails
    }
});
