import { Logger } from "./logger.js";
var logger = new Logger("main", Logger.LOG_LEVELS.FINEST);


var photoList = [];

const photoElement = document.getElementById("photo");
const containerInfo = document.getElementById("photo-info");
const containerButtons = document.getElementById("photo-controls");

let currentIndex = 0;

async function fetchXMLData() {
    let log = logger.createSubLogger("fetchXMLData");
    log.info(`Fetching photo data from xml file`);

    await fetch("../xml/photos.xml")
        .then((response) => response.text())
        .then((text) => {
            const parser = new DOMParser();
            const xmlDocument = parser.parseFromString(text, "text/xml");
        
            const elements = xmlDocument.getElementsByTagName("photo");
            log.debug(`Found ${elements.length} entrie/s in xml file.`);
            
            for (let i = 0; i < elements.length; i++) {
                let element = elements.item(i);

                let photo = {}
                photo.fileName = readData(element, "fileName");
                photo.dateTime = formatDate(readData(element, "dateTime"));
                let cameraMake = readData(element, "cameraMake");
                let cameraModel = readData(element, "cameraModel");
                photo.camera = `${cameraMake} ${cameraModel}`;
                photo.lensModel = readData(element, "lensModel");
                photo.imageWidth = readData(element, "imageWidth");
                photo.imageHeight = readData(element, "imageHeight");
                photo.iso = readData(element, "iso");
                photo.focalLength = readData(element, "focalLength");
                photo.fNumber = readData(element, "fNumber");
                photo.exposureTime = readData(element, "exposureTime");

                photoList.push(photo);
            }
    })

    log.info(`Finished reading in photo information`);
}
function readData(element, tagName) {
    return element.getElementsByTagName(tagName).item(0).innerHTML;
}
function formatDate(date) {
    return date.replace("T", " ");
}
function keyToReadableString(key) {
    switch (key) {
        case "dateTime": return "Datum";
        case "camera": return "Kamera";
        case "lensModel": return "Objektiv";
        case "imageWidth": return "Bildbreite";
        case "imageHeight": return "Bildhöhe";
        case "iso": return "ISO";
        case "focalLength": return "Brennweite";
        case "fNumber": return "Blendenzahl";
        case "exposureTime": return "Belichtungszeit";
        default: return "Unbekannt";
    }
}

function switchToPhoto(index) {
    let log = logger.createSubLogger("switchToPhoto");
    log.info(`Switching to photo ${index}.`);
    log.debug(`Number of photos in list: ${photoList.length}`);

    if (!(index in photoList)) {
        log.error(`Unable to retrieve photo information for index ${index}!`);
        return;
    }
    let photo = photoList[index];
    log.debug(`Photo to switch to: ${JSON.stringify(photo)}`);

    photoElement.src = `../images/photos/${photo["fileName"]}`;
    let infoList = document.createElement("ul");

    for (const key in photo) {
        log.fine(`  Retrieving information for key '${key}':`);
        if (key == "fileName") { continue; }

        infoList.appendChild(createListItem(`${keyToReadableString(key)}: ${photo[key]}`));
    }

    containerInfo.innerHTML = "";
    containerInfo.appendChild(infoList);
}
function createListItem(content) {
    let listItem = document.createElement("li");
    listItem.innerText = content;
    return listItem;
}

function createControlButtons() {
    containerButtons.innerHTML = "";

    let button = document.createElement("button");
    button.innerText = "Erstes";
    button.addEventListener("click", switchToFirstPhoto);
    containerButtons.appendChild(button);

    button = document.createElement("button");
    button.innerText = "<--";
    button.addEventListener("click", switchToPrevPhoto);
    containerButtons.appendChild(button);

    button = document.createElement("button");
    button.innerText = "-->";
    button.addEventListener("click", switchToNextPhoto);
    containerButtons.appendChild(button);

    button = document.createElement("button");
    button.innerText = "Letztes";
    button.addEventListener("click", switchToLastPhoto);
    containerButtons.appendChild(button);
}

function switchToFirstPhoto() {
    currentIndex = 0;
    switchToPhoto(currentIndex);
}
function switchToLastPhoto() {
    currentIndex = photoList.length - 1;
    switchToPhoto(currentIndex);
}
function switchToNextPhoto() {
    if (currentIndex+1 < photoList.length) {
        currentIndex++;
    }
    switchToPhoto(currentIndex);
}
function switchToPrevPhoto() {
    if (currentIndex-1 >= 0) {
        currentIndex--;
    }
    switchToPhoto(currentIndex);
}

await fetchXMLData();
createControlButtons();
switchToFirstPhoto();