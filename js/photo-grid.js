const divPhotoGrid = document.getElementById("photo-grid");

const modalContainer = document.getElementById('modal-container');
const modalImage = document.getElementById('modal-content');
const modalClose = document.getElementById('modal-close');





modalClose.addEventListener("click", () => {
    modalContainer.style.display = "none";
})
function displayImage(image) {
    modalContainer.style.display = "flex";
    modalImage.src = image.src;
    modalImage.alt = image.alt;
    modalImage.addEventListener("click", () => {
        modalContainer.style.display = "none";
    })
}