document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", (e) => {
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // ✅ Email format validation
        const emailPattern = /^[\w\.-]+@[\w\.-]+\.\w{2,4}$/;
        if (!emailPattern.test(email)) {
            e.preventDefault();
            errorMessage.textContent = "Please enter a valid email like someone@example.com.";
            return;
        }

        // ✅ Password strength validation
        const passwordError = checkPassword(password);
        if (passwordError) {
            e.preventDefault();
            errorMessage.textContent = passwordError;
            return;
        }

        // ✅ Password match validation
        if (password !== confirmPassword) {
            e.preventDefault();
            errorMessage.textContent = "Passwords do not match!";
            return;
        }

        // ✅ If all is good
        errorMessage.textContent = ""; // Clear previous errors
        alert("Sign in Successful!");
        // If you want to prevent real form submission and go to main.html:
        e.preventDefault();
        window.location.href = "Main.html";
    });
});

// Function to check password strength
function checkPassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (password.length < minLength || !hasUpperCase || !hasNumber || !hasSpecialChar) {
        return "Password must be at least 8 characters long, with one uppercase letter, one number, and one special character.";
    }
    return null;
}
