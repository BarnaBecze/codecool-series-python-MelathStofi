function apiGet(url, callback) {
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin'
    })
        .then(response => response.json())
        .then(response => callback(response))
}


function modifyQueryResult(queryResult) {
    let shows = [];
    let _id = null;
    let count = -1;
    for (const show of queryResult) {
        if (show['id'] === _id) {
            shows[count]['genre'] += `, ${show['genre']}`;
        }
        else {
            _id = show['id'];
            shows.push(show);
            count += 1;
        }
    }
    return shows
}


function pasteShows(shows) {
    const tbody = document.getElementsByTagName('tbody');
    tbody.innerHTML = "";

    for (const show of shows) {
        tbody.innerHTML += `<td>${show.title}</td>
                            <td>${show.year}</td>
                            <td>${show.runtime}</td>
                            <td>${show.genre}</td>
                            <td>${show.rating}</td>
                            <td><a href="${show.trailer}" target="_blank">${show.trailer}</a></td>
                            <td><a href="${show.homepage}" target="_blank">${show.homepage}</a></td>`
    }
}


function main() {
    const nextButton = document.querySelector('#next-button');
    nextButton.addEventListener('click', () => apiGet('/get-15-shows', (response) => {
        const shows = modifyQueryResult(response);
        pasteShows(shows);}));
    apiGet('/get-15-shows', (response) => {
        const shows = modifyQueryResult(response);
        pasteShows(shows);})
}


main();
