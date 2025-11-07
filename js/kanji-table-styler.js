const ROWS_PER_ENTRY = 4;
const table = document.getElementById("kanji-table");

for (let i = 1; i < table.rows.length; i++) {
    let paintIndex = i % (ROWS_PER_ENTRY*2);
    if (paintIndex < ROWS_PER_ENTRY) {
        table.rows.item(i).classList.add("darker");
    }
}