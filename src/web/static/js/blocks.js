let updateAllBlocks = window.setInterval(async function () {
    await blocksLoad()
}, 5000);

let blocksOnPage = 15

function range(size, startAt = 0) {
    return [...Array(size).keys()].map(i => i + startAt);
}

function getCurrentPage() {
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
        if (x === currentPage) {
            pagesObject.innerHTML +=
                `<li class="page-item disabled"><a class="page-link" href="/blocks?page=${x}">${x}</a></li>`
        } else {
            pagesObject.innerHTML +=
                `<li class="page-item"><a class="page-link" href="/blocks?page=${x}">${x}</a></li>`
        }

    }


    if (currentPage === pagesCount || pagesCount === 0) {
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


async function blocksLoad(force = false) {
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
            <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">
${block['block_hash']}</td>
            <td><a href="/block/${block['block_hash']}">Подробнее</a></td>`
        let newBlock = document.createElement('tr');
        newBlock.innerHTML = code
        blocksObject.prepend(newBlock)
    }

    await updatePages(response["total_count"])

    let nodeButton = document.getElementById("dropdownMenuButton")
    let nodes = document.getElementById("nodes")

    let transactionData = await (await fetch("/get_transaction_data", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            node: currentNode,
            transaction: ""
        })
    })).json()

    if (force) {
        if (!transactionData["status"] && !transactionData["node_none"]) {
            document.getElementById("errorNodeText").innerText = `Не получилось подключиться к ноде ${currentNode}. Выберите другую.`
            $("#errorPopupNode").toast('show'); // Показываем popup
            setTimeout(function () {
                $("#errorPopupNode").toast('hide'); // Скрываем popup через 2 секунды
            }, 2000);
        }

        if (transactionData["status"]) {
            document.getElementById("successNodeText").innerText = `Успешно подключились к ноде ${currentNode}`
            $("#successChangeNode").toast('show');
            setTimeout(function () {
                $("#successChangeNode").toast('hide');
            }, 2000);
        }
    }

    if (!currentNode) {
        let active_nodes = []
        for (let node of transactionData["nodes"]) {
            if (node["is_online"]) {
                active_nodes.push(node)
            }
        }

        let randomNode;
        if (active_nodes.length > 0) {
            randomNode = active_nodes[Math.floor(Math.random() * active_nodes.length)];
        } else {
            randomNode = transactionData["nodes"][Math.floor(Math.random() * transactionData["nodes"].length)];
        }
        nodeButton.textContent = randomNode["title_id"]
        localStorage.setItem(uniqueKey("node"), randomNode["title_id"])
        await blocksLoad(true)
    } else {
        nodeButton.textContent = currentNode
        nodes.innerHTML = ""

        for (const node of transactionData["nodes"]) {
            let status = node["is_online"] ? "🟢" : "🔴"
            nodes.innerHTML += `<a class="dropdown-item" href="#" 
        onclick="setNode('${node["title_id"]}')">${status} ${node["title_id"]} (Блоков: ${node["blocks_count"]})</a>`
        }
    }
}

function is_numeric(str) {
    return /^\d+$/.test(str);
}

async function searchAll() {
    let searchQuery = document.getElementById("searchData").value
    let currentNode = localStorage.getItem(uniqueKey("node"))

    if (!searchQuery) {
        return
    }

    if (searchQuery.length === 62 && searchQuery.startsWith("poa")) {
        window.open(`/address/${searchQuery}`, '_blank');
    }

    if (searchQuery.length === 64) {
        let transactionData = await (await fetch("/get_transaction_data", {
            method: 'POST', headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                node: currentNode,
                transaction: searchQuery
            })
        })).json()

        console.log(transactionData)

        if (transactionData["transaction_data"]["transaction"]) {
            window.open(`/transaction/${searchQuery}`,
                "_blank")
            return
        }


        let blockData = await (await fetch("/get_block_data", {
            method: 'POST', headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                node: currentNode,
                block: searchQuery
            })
        })).json()

        if (blockData["block_data"]["block"]) {
            window.open(`/block/${blockData['block_data']['block']['block_hash']}`, "_blank")
            return
        }

        return
    }

    if (is_numeric(searchQuery)) {
        let blockData = await (await fetch("/get_block_by_number", {
            method: 'POST', headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                node: currentNode,
                block_number: searchQuery
            })
        })).json()

        if (!blockData["block_data"]["block"]) {
            return
        }

        window.open(`/block/${blockData['block_data']['block']['block_hash']}`, "_blank")
    }
}


async function setNode(node) {
    let nodeButton = document.getElementById("dropdownMenuButton")
    nodeButton.textContent = node
    localStorage.setItem(uniqueKey("node"), node)

    await blocksLoad(true)
}