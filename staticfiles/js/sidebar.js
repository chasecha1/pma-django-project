const toggler = document.querySelector(".toggler-btn");
const sidebar = document.querySelector("#sidebar");
const footer = document.querySelector('footer');
if (!footer) {
   console.log("Footer element not found.");
}

// Function to manage sidebar state on page load or resize
function adjustSidebar() {
    const screenWidth = window.innerWidth;
    sidebar.style.transition = "none";

    // Retrieve the collapsed state from localStorage
    const collapsedState = localStorage.getItem("collapsedState") === "true";


    // Apply the saved collapsed state, unless on a small screen
    if (screenWidth > 768) {
        if (collapsedState) {
            sidebar.classList.add("collapsed");
            footer.style.marginLeft = '60px';
        } else {
            sidebar.classList.remove("collapsed");
            footer.style.marginLeft = '264px';
        }
    } else {
        // Automatically collapse sidebar on small screens
        sidebar.classList.add("collapsed");
        footer.style.marginLeft = '60px';
    }

    setTimeout(() => {
        sidebar.style.transition = "";
    }, 50);
}

// Event listener for toggling sidebar on button click
if (toggler) {
    toggler.addEventListener("click", function () {
        // Toggle the collapsed class
        sidebar.classList.toggle("collapsed");

        // Save the current state to localStorage
        const isCollapsed = sidebar.classList.contains("collapsed");
        localStorage.setItem("collapsedState", isCollapsed);
        if (isCollapsed) {
            footer.style.marginLeft = '60px';
        } else {
            footer.style.marginLeft = '264px';
        }
    });
}

// Add event listener to handle window resize
window.addEventListener("resize", adjustSidebar);

// Call the function on initial load to set the correct state
adjustSidebar();

// show tooltips
document.addEventListener("DOMContentLoaded", function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
