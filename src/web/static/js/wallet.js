let updateAll = window.setInterval(async function () {
    console.log("update")
    await setData(true)
}, 3000);


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


function createTransaction() {
    let code = `<div class="card mb-1">
            <div class="card-body">
                <div class="container">
                    <div class="row mb-2">
                        <p class="card-text">
                            <span class="transaction-type-arrow green-arrow">&rarr;</span>
                            <span class="transaction-amount">+10 POA</span>
                        </p>
                    </div>
                    <div class="row mb-2">
                        <p class="card-text">
                            <span class="transaction-address">poa1q...rxpu3</span>
                            <button id="cfs" type="button" class="btn-sm btn-secondary" onClick="copySign()">
                                Копировать адрес
                            </button>
                        </p>
                    </div>
                    <div class="row mb-2">
                        <p class="card-text transaction-date">2024-04-12 15:30:00</p>
                    </div>
                    <div class="row">
                        <p class="card-text"><a href="#">Перейти к транзакции</a></p>
                    </div>
                </div>
            </div>

        </div>`

    const newTrans = document.createElement('div');
    newTrans.class = "card mb-1"
    newTrans.innerHTML = code
    return newTrans
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
    })).json())["encoded_transaction"]

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


function openTab(tabName) {
    let openTab = document.getElementById(tabName)

    let closeTab, openLink, closeLink;
    if (openTab.id === "send") {
        closeTab = document.getElementById("sign")
        openLink = document.getElementById("sendlink")
        closeLink = document.getElementById("signlink")
    } else {
        closeTab = document.getElementById("send")
        openLink = document.getElementById("signlink")
        closeLink = document.getElementById("sendlink")
    }

    openTab.hidden = false
    openLink.className = "nav-link active"

    closeTab.hidden = true
    closeLink.className = "nav-link"
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

async function setData(forUpdate = false) {
    let addressText = document.getElementById("address")
    let balanceText = document.getElementById("balance")
    let nodes = document.getElementById("nodes")

    let currentNode = localStorage.getItem(uniqueKey("node"))

    let walletData = await (await fetch("/get_wallet_data", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            node: currentNode,
            address: localStorage.getItem(uniqueKey("address"))
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

    addressText.textContent = walletData["address"]
    balanceText.textContent = `${walletData["balance"]} POA`

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

        let transactions = []

        let transactionsObject = document.getElementById("transactions")

        transactionsObject.appendChild(createTransaction())
        transactionsObject.appendChild(createTransaction())
        transactionsObject.appendChild(createTransaction())
        transactionsObject.appendChild(createTransaction())
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