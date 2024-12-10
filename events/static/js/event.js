// Function to open the file in a new tab
function viewFile(url) {
    console.log(url);
    window.open(url, '_blank');
}

// Function to delete the file
function deleteFile(fileId) {
    if (confirm('Are you sure you want to delete this file?')) {
        fetch("{% url 'delete_file' 0 %}".replace('0', fileId), {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                return response.json().then(data => {
                    alert(data.error || 'Failed to delete the file.');
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips manually
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
