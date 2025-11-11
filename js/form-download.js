// Dieses Script hat die folgende Seite als Grundlage:
// https://developer.mozilla.org/en-US/docs/Web/API/Blob


function downloadTextFile() {
    let name = document.getElementById("form-name").value;
    let mail = document.getElementById("form-email").value;
    let message = document.getElementById("form-message").value;

    let txt = [
        "Name: ", name, "\n", 
        "Mail: ", mail, "\n", 
        "Nachricht: ", message];

    var blob = new Blob(txt, { type: 'text/plain' });
    var link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = 'contact-form.txt';
    link.click();
}