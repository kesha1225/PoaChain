
let updateAll = window.setInterval(async function () {
    await setData(true)
}, 3000);


let addedHashes = []
let chosenState = "all"

function setAll() {
    document.getElementById("amount").value =
        document.getElementById("balance").innerText.split(" ")[0]
}

function isvalidAddress(address) {
    return (address.startsWith("poa") && address.length === 62
        && address !== document.getElementById("address").textContent);
}

function isvalidAmount(amount) {
    return (!isNaN(amount) && parseFloat(amount) >= 0.01);
}

function confirmSend() {
    let targetAddress = document.getElementById("recipient")
    let targetAmount = document.getElementById("amount")

    let targetAddressValue = targetAddress.value
    let targetAmountValue = targetAmount.value

    if (!targetAddressValue || !isvalidAddress(targetAddressValue)) {
        targetAddress.classList.add("error");
        setTimeout(function () {
            targetAddress.classList.remove("error");
        }, 2000);
        $("#errorPopupAddress").toast('show');
        setTimeout(function () {
            $("#errorPopupAddress").toast('hide');
        }, 2000);
        return
    }

    if (!targetAmountValue || !isvalidAmount(targetAmountValue)) {
        targetAmount.classList.add("error");
        setTimeout(function () {
            targetAmount.classList.remove("error");
        }, 2000);
        $("#errorPopupAmount").toast('show');
        setTimeout(function () {
            $("#errorPopupAmount").toast('hide');
        }, 2000);
        return;
    }

    document.getElementById("transactionData").innerHTML = `Вы уверены что хотите отправить 
    <code>${targetAmountValue} POA</code> на <code>${targetAddressValue}</code>?`
    $('#confirmModal').modal('show');
}


async function sendTransaction() {
    $('#confirmModal').modal('hide');
    let targetAddress = document.getElementById("recipient").value
    let targetAmount = document.getElementById("amount").value

    let transaction = (await (await fetch("/create_transaction", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            address: targetAddress, amount: targetAmount,
            publicKey: localStorage.getItem(uniqueKey("publicKey")),
            privateKey: localStorage.getItem(uniqueKey("privateKey"))
        })
    })).json())

    if (!transaction["status"]){
        document.getElementById("errorNodeDesc").innerText = "Не удалось отправить транзакцию. Неверные данные."
        $("#errorPopupNodeSend").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNodeSend").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
        return
    }


    transaction = transaction["encoded_transaction"]

    let currentNode = localStorage.getItem(uniqueKey("node"))

    let response = await (await fetch("/send_transaction", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({data: transaction, node: currentNode})
    })).json()

    if (!response["status"]) {
        document.getElementById("errorNodeDesc").innerText = "Не удалось отправить транзакцию. Нода недоступна."
        $("#errorPopupNodeSend").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNodeSend").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
    } else if (!response["result"]["status"]) {
        document.getElementById("errorNodeDesc").innerText = response["result"]["description"]

        $("#errorPopupNodeSend").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNodeSend").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
    } else {
        document.getElementById("recipient").value = ""
        document.getElementById("amount").value = ""


        $("#successPopupNodeSend").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#successPopupNodeSend").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
        await setData(true)
    }

}


async function openTab(tabName) {
    let openTab = document.getElementById(tabName)
    let address = getAddress()

    let currentNode = localStorage.getItem(uniqueKey("node"))
    let closeTab, openLink, closeLink, closeLink2;
    if (openTab.id === "send") {
        closeTab = document.getElementById("sign")
        openLink = document.getElementById("sendlink")
        closeLink = document.getElementById("signlink")
    } else if (openTab.id === "sign") {
        closeTab = document.getElementById("send")
        openLink = document.getElementById("signlink")
        closeLink = document.getElementById("sendlink")
    } else if (openTab.id === "allTrans") {
        openLink = document.getElementById("allTrans")
        closeLink = document.getElementById("receive")
        closeLink2 = document.getElementById("sent")
        await createTransactions(address, currentNode, "all", true)
        chosenState = "all"
    } else if (openTab.id === "receive") {
        openLink = document.getElementById("receive")
        closeLink = document.getElementById("allTrans")
        closeLink2 = document.getElementById("sent")
        await createTransactions(address, currentNode, "to", true)
        chosenState = "to"
    } else if (openTab.id === "sent") {
        openLink = document.getElementById("sent")
        closeLink = document.getElementById("allTrans")
        closeLink2 = document.getElementById("receive")
        await createTransactions(address, currentNode, "from", true)
        chosenState = "from"
    }

    let isMobile = window.innerWidth < 900

    if (openTab) {
        openTab.hidden = false
    }

    openLink.className = "nav-link active"

    if (closeTab) {
        closeTab.hidden = true
    }
    closeLink.className = "nav-link"

    if (closeLink2) {
        closeLink2.className = "nav-link"
    }


    if (isMobile) {
        openLink.className = "nav-link active btn-sm"
        closeLink.className = "nav-link btn-sm"
        closeLink2.className = "nav-link btn-sm"
    }
}


function getAddress() {
    let address = localStorage.getItem(uniqueKey("address"))

    if (window.location.pathname.includes("/address/")) {
        address = window.location.pathname.replace("/address/", "")
    }
    return address
}

function copyAddress() {
    let addressElement = document.getElementById("address");
    let address = addressElement.textContent;
    navigator.clipboard.writeText(address)
        .then(function () {
            $("#successPopup").toast('show'); // Показываем popup
            setTimeout(function () {
                $("#successPopup").toast('hide'); // Скрываем popup через 2 секунды
            }, 2000);
        })
        .catch(function (error) {
        });
}


function isWallet() {
    if (window.location.pathname.includes("/blocks")) {
        return false
    }
    return true
}

async function createTransactions(address, currentNode, type = "all", full_update = false) {
    if (!isWallet()) {
        return
    }

    let transactions = (await (await fetch("/get_transactions", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            node: currentNode,
            address: address,
            type: type
        })
    })).json())["transactions"]

    let transactionsObject = document.getElementById("transactions")

    if (full_update) {
        addedHashes = []
        transactionsObject.innerHTML = ""
        transactionsObject.scrollTo(0, 0);
    }
    for (const transactionObj of transactions) {
        if (addedHashes.includes(transactionObj["transaction_hash"])) {
            continue
        }
        transactionsObject.prepend(createTransaction(transactionObj))
        addedHashes.push(transactionObj["transaction_hash"])
    }
}

async function setData(forUpdate = false) {
    let addressText = document.getElementById("address")
    let balanceText = document.getElementById("balance")
    let nodes = document.getElementById("nodes")

    let currentNode = localStorage.getItem(uniqueKey("node"))

    if (!localStorage.getItem(uniqueKey("privateKey")) ||
        !localStorage.getItem(uniqueKey("publicKey")) ||
        !localStorage.getItem(uniqueKey("address"))) {
        await logout()
        return
    }

    let address = getAddress()

    let walletData = await (await fetch("/get_wallet_data", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            node: currentNode,
            address: address
        })
    })).json()


    let nodeButton = document.getElementById("dropdownMenuButton")

    if (!walletData["status"] && !walletData["node_none"] && !forUpdate) {
        document.getElementById("errorNodeText").innerText = `Не получилось подключиться к ноде ${currentNode}. Выберите другую.`
        $("#errorPopupNode").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNode").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
    }

    if (walletData["status"] && !forUpdate) {
        document.getElementById("successNodeText").innerText = `Успешно подключились к ноде ${currentNode}`
        $("#successChangeNode").toast('show');
        setTimeout(function () {
            $("#successChangeNode").toast('hide');
        }, 2000);
    }

    if (isWallet()) {
        addressText.textContent = walletData["address"]
        balanceText.textContent = `${walletData["balance"]} POA`
    }


    if (!currentNode) {
        let active_nodes = []
        for (let node of walletData["nodes"]) {
            if (node["is_online"]) {
                active_nodes.push(node)
            }
        }

        let randomNode;
        if (active_nodes.length > 0) {
            randomNode = active_nodes[Math.floor(Math.random() * active_nodes.length)];
        } else {
            randomNode = walletData["nodes"][Math.floor(Math.random() * walletData["nodes"].length)];
        }
        nodeButton.textContent = randomNode["title_id"]
        localStorage.setItem(uniqueKey("node"), randomNode["title_id"])
        await setData()
    } else {
        nodeButton.textContent = currentNode
        nodes.innerHTML = ""

        for (const node of walletData["nodes"]) {
            let status = node["is_online"] ? "🟢" : "🔴"
            nodes.innerHTML += `<a class="dropdown-item" href="#" 
        onclick="setNode('${node["title_id"]}')">${status} ${node["title_id"]} (Блоков: ${node["blocks_count"]})</a>`
        }
        await createTransactions(address, currentNode, chosenState)
    }

}

async function setNode(node) {
    let nodeButton = document.getElementById("dropdownMenuButton")
    nodeButton.textContent = node
    localStorage.setItem(uniqueKey("node"), node)

    await setData()
}


async function signMessage() {
    let message = document.getElementById("message")

    let result = (await (await fetch("/sign", {
        method: "POST",
        body: JSON.stringify({
            message: message.value,
            private_key: localStorage.getItem(uniqueKey("privateKey"))
        })
    })).json())["result"]

    let signText = document.getElementById("resultSign")

    signText.hidden = false
    signText.value = result

    document.getElementById("signButton").hidden = false
}


async function copySign() {
    await signMessage()
    let signElement = document.getElementById("resultSign");
    let sign = signElement.value;
    navigator.clipboard.writeText(sign)
        .then(function () {
            $("#successPopupSign").toast('show'); // Показываем popup
            setTimeout(function () {
                $("#successPopupSign").toast('hide'); // Скрываем popup через 2 секунды
            }, 2000);
        })
        .catch(function (error) {
        });
}

async function copyTransAddress(address) {
    navigator.clipboard.writeText(address)
        .then(function () {
            $("#successPopup").toast('show'); // Показываем popup
            setTimeout(function () {
                $("#successPopup").toast('hide'); // Скрываем popup через 2 секунды
            }, 2000);
        })
        .catch(function (error) {
        });
}