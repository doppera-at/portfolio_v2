var kanjiTableParse = document.getElementById("kanji-table");

fetch("../xml/kanji-list.xml")
    .then((response) => response.text())
    .then((text) => {
        const parser = new DOMParser();
        const xmlDocument = parser.parseFromString(text, "text/xml");
        const rows = xmlDocument.getElementsByTagName("kanji");

        for (let i = 0; i < rows.length; i++) {
            const row = rows.item(i);

            let tr = document.createElement("tr");
            let td = document.createElement("td");
            td.classList.add("meaning");
            td.innerText = readData(row, "meaning");
            tr.appendChild(td);

            td = document.createElement("td");
            td.rowSpan = 2;
            td.innerText = "Kunyomi:\n" + readData(row, "kunyomi");
            tr.appendChild(td);

            td = document.createElement("td");
            td.rowSpan = 4;
            td.innerText = readData(row, "description");
            tr.appendChild(td);
            kanjiTableParse.appendChild(tr);

            tr = document.createElement("tr");
            td = document.createElement("td");
            td.rowSpan = 3;
            td.lang = "ja";
            td.innerText = readData(row, "character");
            tr.appendChild(td);
            kanjiTableParse.appendChild(tr);

            tr = document.createElement("tr");
            td = document.createElement("td");
            td.rowSpan = 2;
            td.innerText = "Onyomi:\n" + readData(row, "onyomi");
            tr.appendChild(td);
            kanjiTableParse.appendChild(tr);

            tr = document.createElement("tr");
            kanjiTableParse.appendChild(tr);
        
            tr = document.createElement("tr");
            tr.classList.add("spacer");
            td = document.createElement("td");
            td.colSpan = 3;
            tr.appendChild(td);
            kanjiTableParse.appendChild(tr);
        }
    });


function readData(row, tagName) {
    return row.getElementsByTagName(tagName).item(0).innerHTML;
}