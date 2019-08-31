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

function sortTable(type) {
    const titleHeader = event.target;
    let sortDirection = titleHeader.dataset.sortDirection;
    const table = document.getElementById('showsBody');
    const tableData = Array.from(table.children);
    const rows = [];
    let targetColumnNum;
    switch (type) {
        case 'title':
            targetColumnNum = 0;
            break;
        case 'year':
            targetColumnNum = 1;
            break;
        case 'runtime':
            targetColumnNum = 2;
            break;
        case 'genre':
            targetColumnNum = 3;
            break;
        case 'rating':
            targetColumnNum = 4;
            break;
        default: targetColumnNum = 0
    }
    const upArrow = `${titleHeader.innerText}<i class="fas fa-sort-up"></i>`;
    const downArrow = `${titleHeader.innerText}<i class="fas fa-sort-down"></i>`;
    tableData.forEach(row => !row.hidden ? rows.push(row) : '');
    rows.sort((a, b) => {
            return a.querySelectorAll('td')[targetColumnNum].innerHTML.toLowerCase().localeCompare(b.querySelectorAll('td')[targetColumnNum].innerHTML.toLowerCase())
        });
    if (sortDirection === 'desc') {rows.reverse()}
    tableData.forEach(row => !row.hidden ? row.parentElement.removeChild(row) : '');
    rows.forEach(row => table.appendChild(row));
    titleHeader.setAttribute('data-sort-direction',
        sortDirection === 'asc' ? 'desc' : 'asc');
    titleHeader.innerHTML = (sortDirection === 'asc') ? upArrow : downArrow

}

function showMoreDetails() {
    const titles = document.querySelectorAll('#redirectToDetails');
    const titlesArray = Array.from(titles);
    let showDetails = '';
    titlesArray.forEach(title => title.addEventListener('click', () => {
        const url = window.location.host;
        fetch('http://' + url + `/${title.innerText}`)
            .then((resp) => resp.json())
            .then((data) => {
                showDetails = data[0];
                document.querySelector('.col-twothird > h2').innerText = showDetails.title.slice(1, -1);
                document.querySelector('.col-twothird > p').innerHTML = `
                                                                                Avg. runtime: ${showDetails.runtime} min<span class="separator">|</span>
                                                                                ${showDetails.genre.slice(1, -1)} <span class="separator">|</span>
                                                                                ${showDetails.year.slice(1,5)}<span class="separator">|</span>Rating: ${showDetails.rating.slice(1, 5)}`;
                document.querySelector('#overview').innerText = `${showDetails.overview}`;
                document.querySelector('.detailed-view').style.display = 'block'
            })
    }));
}

function main() {
    loadTable();
    expandTable();

    const sorters = document.querySelectorAll('th');
    sorters.forEach(s => {
        s.addEventListener('click', () => {
            sortTable(s.getAttribute('data-sort-type'))
        })
    });
    showMoreDetails()
}

main();