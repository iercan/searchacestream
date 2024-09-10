
function refresh_listeners(){
    let buttons = document.querySelectorAll(".action_icon");

    buttons.forEach(function(elem) {
        console.log(elem);
        elem.addEventListener("click", function(event) {
            console.log(elem);
            event.preventDefault();
            const infohash = elem.getAttribute('data-infohash');
            fetch('/get_content_id', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `infohash=${infohash}`
            })
                .then(response => response.json())
                .then(data => {
                    let textToCopy = '';
                    let pid = 1;
                    let buttonType = elem.getAttribute('data-type');
                    if (buttonType == "network"){
                        pid = Math.floor(Math.random() * 10000) + 1;
                        textToCopy = "http://127.0.0.1:6878/ace/getstream?id=" + data.content_id + "&pid=" + pid;
                    }
                    else if (buttonType == "open"){

                        window.open("acestream://" + data.content_id, '_blank');
                        return;

                    }
                    else{
                        textToCopy = data.content_id;
                    }
                    navigator.clipboard.writeText(textToCopy)
                        .then(() => {
                            let icon_elem = elem.getElementsByTagName("i")[0]
                            icon_elem.classList.add('fa-check');
                            setTimeout(() => {
                                icon_elem.classList.remove('fa-check');
                            }, 2000); // Reset after 2 seconds
                        })
                        .catch(err => {
                            console.error('Failed to copy text: ', err);
                        });
                    //const resultsBody = elem.parentElement;
                    //resultsBody.innerHTML = data.content_id;
                });
        });
    });
}
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${query}`
    })
        .then(response => response.json())
        .then(data => {
            const resultsBody = document.getElementById('resultsBody');
            resultsBody.innerHTML = '';
            if(data.length === 0) {
                resultsBody.innerHTML = 'No results';
                return;
            }
            data.forEach(result => {
                const statusIcon = result.status === 2 ? 'Active' : 'Unstable';
                const row = `<tr>
                        <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-500">${result.name}</td>
                        <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-500">${result.availability}</td>
                        <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-500">${statusIcon}</td>
                        <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-500">${result.languages}</td>
                        <td class="flex items-center px-6 py-4 whitespace-no-wrap border-b border-gray-500">
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
            refresh_listeners();
        });
});
