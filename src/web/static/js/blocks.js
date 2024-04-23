let updateAllBlocks = window.setInterval(async function () {
    await blocksLoad()
}, 3000);

let blocksOnPage = 15

function range(size, startAt = 0) {
    return [...Array(size).keys()].map(i => i + startAt);
}

function getCurrentPage(){
    let currentPage = window.location.search.replace("?page=", "")
    if (!currentPage || currentPage === "1") {
        currentPage = 1
    }
    return parseInt(currentPage)
}

async function updatePages(blocksCount) {
    let pagesCount = Math.floor(blocksCount / blocksOnPage)
    let pagesObject = document.getElementById("pagesData")
    pagesObject.innerHTML = ""

    let currentPage = getCurrentPage()
    if (currentPage === 1) {
        pagesObject.innerHTML += `<li class="page-item disabled">
            <a class="page-link" href="#" tabIndex="-1">&laquo;</a>
        </li>`
        pagesObject.innerHTML += `<li class="page-item disabled">
            <a class="page-link" href="#" tabIndex="-1">Предыдущая</a>
        </li>`
    } else {
        pagesObject.innerHTML += `<li class="page-item">
            <a class="page-link" href="/blocks?page=1" tabIndex="-1">&laquo;</a>
        </li>`
        pagesObject.innerHTML += `<li class="page-item">
            <a class="page-link" href="/blocks?page=${currentPage - 1}" tabIndex="-1">Предыдущая</a>
        </li>`
    }

    let startPage = Math.max(1, currentPage - 3);
    let endPage = Math.min(pagesCount, startPage + 5);

    let pages = range(pagesCount + 2).slice(startPage, endPage + 1)

    for (const x of pages) {
        if (x === currentPage){
            pagesObject.innerHTML +=
            `<li class="page-item disabled"><a class="page-link" href="/blocks?page=${x}">${x}</a></li>`
        }
        else {
            pagesObject.innerHTML +=
            `<li class="page-item"><a class="page-link" href="/blocks?page=${x}">${x}</a></li>`
        }

    }


    if (currentPage === pagesCount) {
        pagesObject.innerHTML += `<li class="page-item disabled">
            <a class="page-link" href="#">Следующая</a>
        </li>`
        pagesObject.innerHTML += `<li class="page-item disabled">
            <a class="page-link" href="#" tabIndex="-1">&raquo;</a>
        </li>`
    } else {
        pagesObject.innerHTML += `<li class="page-item">
            <a class="page-link" href="/blocks?page=${currentPage + 1}">Следующая</a>
        </li>`
        pagesObject.innerHTML += `<li class="page-item">
            <a class="page-link" href="/blocks?page=${pagesCount}" tabIndex="-1">&raquo;</a>
        </li>`
    }

}


async function blocksLoad() {
    let currentNode = localStorage.getItem(uniqueKey("node"))

    let blocksData = await fetch("/blocks_latest",
        {
            method: 'POST', headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                node: currentNode,
                limit: blocksOnPage,
                offset: blocksOnPage * getCurrentPage()
            })
        })

    let response = (await blocksData.json())
    blocksData = response["blocks"]

    let blocksObject = document.getElementById("blockTable")

    blocksObject.innerHTML = ""
    for (let block of blocksData) {
        let code = `
            <th scope="row">${block['block_number']}</th>
            <td>${block['authority_id']}</td>
            <td>${timeConverter(block['timestamp'])}</td>
            <td>${block['block_hash']}</td>
            <td><a href="/block/${block['block_hash']}">Подробнее</a></td>`
        let newBlock = document.createElement('tr');
        newBlock.innerHTML = code
        blocksObject.prepend(newBlock)
    }

    await updatePages(response["total_count"])
}