function previewPhoto(event) {
    const label = document.getElementById('upload-label');
    const file = event.target.files[0];

    // Display selected image as a preview
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            label.innerHTML = `<img src="${e.target.result}" alt="Profile Photo">`;
        };
        reader.readAsDataURL(file);
    }
}