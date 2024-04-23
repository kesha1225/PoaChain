const globalTransaction = window.location.pathname.replace("/transaction/", "")


async function setDataTrans() {
    let nodes = document.getElementById("nodes")

    let currentNode = localStorage.getItem(uniqueKey("node"))

    let nodeButton = document.getElementById("dropdownMenuButton")

    let transactionData = await (await fetch("/get_transaction_data", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            node: currentNode,
            transaction: globalTransaction
        })
    })).json()

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
        await setDataTrans()
    } else {
        nodeButton.textContent = currentNode
        nodes.innerHTML = ""

        for (const node of transactionData["nodes"]) {
            let status = node["is_online"] ? "🟢" : "🔴"
            nodes.innerHTML += `<a class="dropdown-item" href="#" 
        onclick="setNode('${node["title_id"]}')">${status} ${node["title_id"]} (Блоков: ${node["blocks_count"]})</a>`
        }
    }

    if (!transactionData["transaction_data"]){
        return
    }

    let transactionObj = transactionData["transaction_data"]["transaction"]

    console.log(transactionObj)
    let transactionTitleText = document.getElementById("transTitle")
    if (!transactionObj){
        transactionTitleText.innerText = "Транзакция не найдена"
    }
    else {
        let transactionText = document.getElementById("transData")

        transactionTitleText.innerText = "Данные транзакции:"

        console.log(transactionObj)
        transactionText.innerHTML = `
        <br>
        <p>Хеш: ${transactionObj['transaction_hash']}</p>
        <p>От: <a style="color: white" href="/address/${transactionObj["sender_address"]}">
${transactionObj["sender_address"]}</a></p>
        <p>Кому: <a style="color: white" href="/address/${transactionObj["recipient_address"]}" 
        >${transactionObj["recipient_address"]}</a></p>
        <p>Сумма: ${transactionObj['amount'] / 100} POA</p>
        <p>Номер блока: 1337228</p>
        <p>Ответственная нода: блаблабла</p>
        <p>${timeConverter(transactionObj['timestamp'])}</p>
        `
    }

}

async function setNode(node) {
    let nodeButton = document.getElementById("dropdownMenuButton")
    nodeButton.textContent = node
    localStorage.setItem(uniqueKey("node"), node)

    await setDataTrans()
}