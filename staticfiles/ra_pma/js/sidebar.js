const toggler = document.querySelector(".toggler-btn");
toggler.addEventListener("click", function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
})

document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');

    function adjustSidebarHeight() {
        sidebar.style.height = `${window.innerHeight}px`;
    }

    // Adjust sidebar height initially and on window resize
    adjustSidebarHeight();
    window.addEventListener('resize', adjustSidebarHeight);
});
