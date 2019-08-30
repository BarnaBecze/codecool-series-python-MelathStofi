function loadTable() {
    const tableRows = document.getElementById('showsBody').children;
    const tableRowsArray = Array.from(tableRows).slice(0, 15);
    tableRowsArray.forEach(row => row.hidden = false);
}

function expandTable() {
    const button = document.getElementById('showAll');
    if (!button.hidden) {
        button.addEventListener('click', () => {
            let table = Array.from(document.getElementById('showsBody').children);
            table.forEach(row => row.hidden = false);
            button.hidden = true;
            document.getElementById('hideShows').hidden = false;
            shrinkTable()

        })
    }
}

function shrinkTable() {
    const button = document.getElementById('hideShows');
    if (!button.hidden) {
        button.addEventListener('click', () => {
            let table = Array.from(document.getElementById('showsBody').children).slice(15);
            table.forEach(row => row.hidden = true);
            button.hidden = true;
            document.getElementById('showAll').hidden = false;
            expandTable()
        })
    }
}


function main() {
    loadTable();
    expandTable();

}

main();