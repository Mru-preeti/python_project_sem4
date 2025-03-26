// Function to display selected file name
document.getElementById('pdfUpload').addEventListener('change', function(event) {
    const fileName = event.target.files[0]?.name;
    document.getElementById('fileName').innerText = fileName ? `Selected file: ${fileName}` : "";
});

// Function to simulate form submission
function submitPDF() {
    const fileInput = document.getElementById('pdfUpload');
    
    if (fileInput.files.length === 0) {
        alert("Please select a PDF file before submitting.");
        return;
    }
    
    alert("PDF Submitted! (Processing will be implemented in backend)");
}