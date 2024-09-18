document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    const process_img = document.getElementById('process_img');
    const resultsBody = document.getElementById('results-body');
    const resultTable = document.getElementById('results-table');
    let clipboard = new ClipboardJS('.copy_icon');

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
                let pid = Math.floor(Math.random() * 10000) + 1;
                const row = `<tr>
                        <td class="px-3 py-4 whitespace-no-wrap border-b border-gray-500">${result.name}</td>
                        <td class="px-3 py-4 whitespace-no-wrap border-b border-gray-500 flex flex-col sm:flex-row sm:space-x-2">
                            <a title="Play channel" href="acestream://${result.content_id}" target="_blank" class="action_icon py-1 px-2 rounded focus:outline-none focus:shadow-outline">
                                <i class="fa-lg fa-solid fa-circle-play"></i>
                            </a>
                            <span title="Copy content id to clipboard" data-clipboard-text="${result.content_id}" data-icon="fa-clipboard" class="action_icon copy_icon py-1 px-2 rounded focus:outline-none focus:shadow-outline">
                                <i class="fa-lg fa-solid fa-clipboard"></i>
                            </span>
                            <span title="Copy network url for local media players" data-clipboard-text="http://127.0.0.1:6878/ace/getstream?id=${result.content_id}&pid=${pid}" data-icon="fa-file-video" class="action_icon copy_icon py-1 px-2 rounded focus:outline-none focus:shadow-outline">
                                <i class="fa-lg fa-solid fa-file-video"></i>
                            </span>
                         </td>
                    </tr>`;
                resultsBody.innerHTML += row;
            });
            process_img.style.display = 'none';
            resultTable.hidden = false;
            clipboard.destroy();
            clipboard = new ClipboardJS('.copy_icon');
            clipboard.on('success', function(e) {
                console.info('Action:', e.action);
                console.info('Text:', e.text);
                console.info('Trigger:', e.trigger);
                let elem = e.trigger;
                let icon_orig_class = elem.getAttribute('data-icon');
                let icon_elem = elem.getElementsByTagName("i")[0];
                icon_elem.classList.remove(icon_orig_class);
                icon_elem.classList.add('fa-clipboard-check');
                setTimeout(() => {
                    icon_elem.classList.remove('fa-clipboard-check');
                    icon_elem.classList.add(icon_orig_class);
                }, 1000);
            });
        });
});
