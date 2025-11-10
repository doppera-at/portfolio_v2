const divPhotoGrid = document.getElementById("photo-grid");

const modalContainer = document.getElementById('modal-container');
const modalImage = document.getElementById('modal-content');
const modalClose = document.getElementById('modal-close');

var photoList = [];

async function fetchXMLData() {
    console.log("fetching xml data");
    await fetch("../xml/art.xml")
        .then((response) => response.text())
        .then((text) => {
            const parser = new DOMParser();
            const xmlDocument = parser.parseFromString(text, "text/xml");

            const elements = xmlDocument.getElementsByTagName("photo");
            console.log(`Found ${elements.length} elements in xml file`);
            
            for (let i = 0; i < elements.length; i++) {
                let element = elements.item(i);

                let photo = {};
                photo["fileName"] = element.getElementsByTagName("fileName").item(0).innerHTML;
                photo["description"] = "Sample Alt-Text";
            
                photoList.push(photo);
            }
        })
}

function createPhotoGrid() {
    console.log("Creating photo grid");
    let divPhotoGrid = document.getElementById("photo-grid");
    
    for (let photo of photoList) {
        let image = document.createElement("img");
        image.src = `../images/art/thumbnails/${photo["fileName"]}`;
        image.alt = photo["description"];
        image.id = photo["fileName"];
        image.addEventListener("click", displayImageEvent);
        divPhotoGrid.appendChild(image);
    }
}



modalClose.addEventListener("click", () => {
    modalContainer.style.display = "none";
})
function displayImageEvent(event) {
    displayImage(event.target);
}
function displayImage(image) {
    modalContainer.style.display = "flex";
    modalImage.src = image.src;
    modalImage.alt = image.alt;
    modalImage.addEventListener("click", () => {
        modalContainer.style.display = "none";
    })
}


await fetchXMLData();
createPhotoGrid();