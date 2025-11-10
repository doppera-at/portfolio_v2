/*
For this script, I used the following example as a template:
https://www.w3schools.com/CSS/tryit.asp?filename=trycss_image_gallery_responsive_js
*/


const modalContainer = document.getElementById('modal-container');
const modalImage = document.getElementById('modal-content');
const modalClose = document.getElementById('modal-close');
// const modalCaption = document.getElementById('modal-caption');

modalClose.onclick = function() {
    imageModal.style.display = "none";
}


function displayModal(img) {
    modalContainer.style.display = "block";
    modalImage.src = img.src;
    modalImage.alt = img.alt;
}

