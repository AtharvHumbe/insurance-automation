document.addEventListener('DOMContentLoaded', function() {
    const pdfViewer = document.getElementById('pdf-viewer');
    const pdfInput = document.getElementById('pdf-input');

    // Event listener to change the PDF when a new file is selected
    pdfInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const url = URL.createObjectURL(file);
        pdfViewer.src = url;
    });
});