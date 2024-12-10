function saveBackgroundColor() {
    const colorSelect = document.getElementById('color-select');
    let selectedColor = colorSelect.value;

    if (selectedColor === 'other') {
        const customColorInput = document.getElementById('custom-color');
        const customColor = customColorInput.value.trim();

        if (isValidHex(customColor)) {
            selectedColor = customColor;
        } else {
            alert("Please enter a valid hex color code.");
            return;
        }
    }

    // Make an AJAX request to save the background color in the user's profile
    fetch('/save-background-color/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Get the CSRF token to make the POST request safe
        },
        body: JSON.stringify({
            'background_color': selectedColor
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.body.style.backgroundColor = selectedColor;
            const elementsToStyle = document.querySelectorAll('.content.flex-grow-1');
            elementsToStyle.forEach(element => {
                element.style.backgroundColor = selectedColor;
            });
            window.location.reload();
            alert("Background color saved successfully!");
        } else {
            alert("There was an error saving the background color.");
        }
    })
    .catch(error => {
        alert("An error occurred: " + error);
    });
}
function saveColorForAnonymousUser() {
    // Save the selected color to localStorage for anonymous users
    console.log('Function saveBackgroundColor is loaded');
    const colorSelect = document.getElementById('color-select');
    let selectedColor = colorSelect.value;

    if (selectedColor === 'other') {
        const customColorInput = document.getElementById('custom-color');
        const customColor = customColorInput.value.trim();

        if (isValidHex(customColor)) {
            selectedColor = customColor;
        } else {
            alert("Please enter a valid hex color code.");
            return;
        }
    }

    document.body.style.backgroundColor = selectedColor;
    // Save the selected color to localStorage for anonymous users
    localStorage.setItem('backgroundColor', selectedColor);
    window.location.reload();
    alert("Background color saved locally for anonymous user!");
}

// Utility function to get the CSRF token from the cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function isValidHex(hex) {
    const hexRegex = /^#([0-9A-Fa-f]{3}){1,2}$/;
    return hexRegex.test(hex);
}

function handleColorChange() {
    const colorSelect = document.getElementById('color-select');
    const customColorContainer = document.getElementById('custom-color-container');

    if (colorSelect.value === 'other') {
        // Show the input field for custom color
        customColorContainer.style.display = 'block';
    } else {
        // Hide the input field when a predefined color is selected
        customColorContainer.style.display = 'none';
    }
}

// Add event listener to trigger color change handling when the dropdown value changes
document.getElementById('color-select').addEventListener('change', handleColorChange);


handleColorChange();


function sendMessage() {
    const message = document.getElementById('message').value;
    console.log(message)
    if (message != "") {
        alert("Profile message updated."); //will add bio_text field to userprofile model to allow profile to display text in next commit
    }
    else {
        alert("Please enter a message before submitting.")
    }
}

