document.addEventListener('DOMContentLoaded', function () {
    var toggler = document.querySelector('.navbar-toggler');
    var sidebar = document.getElementById('sidebar');
    console.log("Inside")
    toggler.addEventListener('click', function () {
        sidebar.classList.toggle('sidebar-show');
        console.log("clicked")
    });
});
