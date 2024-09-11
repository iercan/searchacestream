function handle_clipboard(textToCopy, elem, orig_icon_class){
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            let icon_elem = elem.getElementsByTagName("i")[0]
            icon_elem.classList.remove(orig_icon_class);
            icon_elem.classList.add('fa-clipboard-check');
            setTimeout(() => {
                icon_elem.classList.remove('fa-clipboard-check');
                icon_elem.classList.add(orig_icon_class);
            }, 1000);
        })
        .catch(err => {
            console.error('Failed to copy text: ', err);
        });

}

function refresh_listeners(){
    let buttons = document.querySelectorAll(".action_icon");

    buttons.forEach(function(elem) {
        elem.addEventListener("click", function(event) {
            event.preventDefault();
            const infohash = elem.getAttribute('data-infohash');
            let buttonType = elem.getAttribute('data-type');

            if (buttonType == "network"){
                let pid = Math.floor(Math.random() * 10000) + 1;
                handle_clipboard("http://127.0.0.1:6878/ace/getstream?infohash=" + infohash + "&pid=" + pid, elem, "fa-file-video");
                return;
            }

            const url = new URL('/get_content_id', window.location.origin);
            url.searchParams.append('infohash', infohash);
            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (buttonType == "open"){
                        window.open("acestream://" + data.content_id, '_blank');
                        return;
                    }
                    else{
                        textToCopy = data.content_id;
                        handle_clipboard(data.content_id, elem, "fa-clipboard");
                    }
                });
        });
    });
}
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    const process_img = document.getElementById('process_img');
    const resultsBody = document.getElementById('results-body');
    const resultTable = document.getElementById('results-table');

    process_img.style.display = 'grid';
    const url = new URL('/search', window.location.origin);
    url.searchParams.append('query', query);

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
        .then(response => {
            if (!response.ok) {
                resultsBody.innerHTML = 'An error occured while getting data. Error code: ' + response.status ;
                process_img.style.display = 'none';
            }
                return response.json();
            })
        .then(data => {
            resultsBody.innerHTML = '';
            if(data.length === 0) {
                resultsBody.innerHTML = 'No results';
            }
            data.forEach(result => {
                const row = `<tr>
                        <td class="px-3 py-4 whitespace-no-wrap border-b border-gray-500">${result.name}</td>
                        <td class="px-3 py-4 whitespace-no-wrap border-b border-gray-500 flex flex-col sm:flex-row sm:space-x-2">
                            <span title="Play channel" data-infohash="${result.infohash}" data-type="open" class=" action_icon py-1 px-2 rounded focus:outline-none focus:shadow-outline">
                                <i class="fa-lg fa-solid fa-circle-play"></i>
                            </span>
                            <span title="Copy content id to clipboard" data-infohash="${result.infohash}" data-type="copy" class=" action_icon py-1 px-2 rounded focus:outline-none focus:shadow-outline">
                                <i class="fa-lg fa-solid fa-clipboard"></i>
                            </span>
                            <span title="Copy network url for local media players" data-infohash="${result.infohash}" data-type="network" class=" action_icon py-1 px-2 rounded focus:outline-none focus:shadow-outline">
                                <i class="fa-lg fa-solid fa-file-video"></i>
                            </span>
                         </td>
                    </tr>`;
                resultsBody.innerHTML += row;
            });
            process_img.style.display = 'none';
            resultTable.hidden = false;
            refresh_listeners();
        });
});
