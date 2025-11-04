/*
For this script, I used the following example as a template:
https://www.w3schools.com/CSS/tryit.asp?filename=trycss_image_gallery_responsive_js
*/


const imageModal = document.getElementById('modal-imageexpand');
const closeModal = document.getElementById('modal-imageexpand-close');

closeModal.onclick = function() {
    imageModal.style.display = "none";
}

