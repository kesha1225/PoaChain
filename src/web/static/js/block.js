const globalBlock = window.location.pathname.replace("/block/", "")


async function setDataBlock() {
    let nodes = document.getElementById("nodes")

    let currentNode = localStorage.getItem(uniqueKey("node"))

    let nodeButton = document.getElementById("dropdownMenuButton")

    let blockData = await (await fetch("/get_block_data", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            node: currentNode,
            block: globalBlock
        })
    })).json()


    if (!blockData["status"] && !blockData["node_none"]) {
        document.getElementById("errorNodeText").innerText = `Не получилось подключиться к ноде ${currentNode}. Выберите другую.`
        $("#errorPopupNode").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNode").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
    }

    if (blockData["status"]) {
        document.getElementById("successNodeText").innerText = `Успешно подключились к ноде ${currentNode}`
        $("#successChangeNode").toast('show');
        setTimeout(function () {
            $("#successChangeNode").toast('hide');
        }, 2000);
    }

    if (!currentNode) {
        let active_nodes = []
        for (let node of blockData["nodes"]) {
            if (node["is_online"]) {
                active_nodes.push(node)
            }
        }

        let randomNode;
        if (active_nodes.length > 0) {
            randomNode = active_nodes[Math.floor(Math.random() * active_nodes.length)];
        } else {
            randomNode = blockData["nodes"][Math.floor(Math.random() * blockData["nodes"].length)];
        }
        nodeButton.textContent = randomNode["title_id"]
        localStorage.setItem(uniqueKey("node"), randomNode["title_id"])
        await setDataTrans()
    } else {
        nodeButton.textContent = currentNode
        nodes.innerHTML = ""

        for (const node of blockData["nodes"]) {
            let status = node["is_online"] ? "🟢" : "🔴"
            nodes.innerHTML += `<a class="dropdown-item" href="#" 
        onclick="setNode('${node["title_id"]}')">${status} ${node["title_id"]} (Блоков: ${node["blocks_count"]})</a>`
        }
    }

    if (!blockData["block_data"]) {
        return
    }

    let blockObj = blockData["block_data"]["block"]

    let transactionTitleText = document.getElementById("transTitle")
    if (!blockObj) {
        transactionTitleText.innerText = "Блок не найден"
    } else {
        let transactionText = document.getElementById("transData")

        transactionTitleText.innerText = "Данные блока:"

        transactionText.innerHTML = `
        <br>
        <p>Номер: ${blockObj['block_number']}</p>
        <p>Хеш: ${blockObj['block_hash']}</p>
        <p>Издатель: ${blockObj['authority_id']}</p>
        <p>Предыдущий хеш: <a href="/block/${blockObj['previous_hash']}">${blockObj['previous_hash']}</a></p>
        <p>${timeConverter(blockObj['timestamp'])}</p>
        `
    }

}


async function setNode(node) {
    let nodeButton = document.getElementById("dropdownMenuButton")
    nodeButton.textContent = node
    localStorage.setItem(uniqueKey("node"), node)

    await setDataBlock()
}