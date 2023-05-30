// Trefle API
document.querySelector(".btn.btn-outline-success").addEventListener("click", function(event){
    event.preventDefault(); // Prevent the form from being submitted normally
    const searchTerm = document.querySelector('.form-control.me-2').value;
    window.location.href = `page2.html?q=${searchTerm}`;

});
