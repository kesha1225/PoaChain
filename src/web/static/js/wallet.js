function isvalidAddress(address) {
    return (address.startsWith("poa") && address.length === 62
        && address !== document.getElementById("address").textContent);
}

function isvalidAmount(amount) {
    return (!isNaN(amount));
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

    console.log(targetAddress)
    let transaction = (await (await fetch("/create_transaction", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({address: targetAddress, amount: targetAmount,
        publicKey: localStorage.getItem(uniqueKey("publicKey")),
            privateKey: localStorage.getItem(uniqueKey("privateKey"))})
    })).json())["encoded_transaction"]

    let currentNode = localStorage.getItem(uniqueKey("node"))

    console.log(currentNode)

    let response = await (await fetch("/send_transaction", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({data: transaction, node: currentNode})
    })).json()


    console.log(response)
    if (!response["status"]) {
        $("#errorPopupNodeSend").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNodeSend").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
        return
    }
}

let currentNodes = []


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


async function setData() {
    let addressText = document.getElementById("address")
    let balanceText = document.getElementById("balance")
    let nodes = document.getElementById("nodes")

    let currentNode = localStorage.getItem(uniqueKey("node"))

    let walletData = await (await fetch("/get_wallet_data", {
        method: 'POST', headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({node: currentNode,
            address: localStorage.getItem(uniqueKey("address"))})
    })).json()

    for (const node of walletData["nodes"]) {
        if (currentNodes.includes(node)) {
            continue
        }

        currentNodes.push(node)
        nodes.innerHTML += `<a class="dropdown-item" href="#" onclick="setNode(this)">${node}</a>`
    }

    let nodeButton = document.getElementById("dropdownMenuButton")
    if (!currentNode) {
        let randomNode = walletData["nodes"][Math.floor(Math.random() * walletData["nodes"].length)];
        nodeButton.textContent = randomNode
        localStorage.setItem(uniqueKey("node"), randomNode)
    }

    if (!walletData["status"]) {
        $("#errorPopupNode").toast('show'); // Показываем popup
        setTimeout(function () {
            $("#errorPopupNode").toast('hide'); // Скрываем popup через 2 секунды
        }, 2000);
    }

    addressText.textContent = walletData["address"]
    balanceText.textContent = `${walletData["balance"]} POA`

    nodeButton = document.getElementById("dropdownMenuButton")

    if (currentNode) {
        nodeButton.textContent = currentNode
    } else {
        let randomNode = walletData["nodes"][Math.floor(Math.random() * walletData["nodes"].length)];
        nodeButton.textContent = randomNode
        localStorage.setItem(uniqueKey("node"), randomNode)
    }
}

async function setNode(node) {
    node = node.innerText
    let nodeButton = document.getElementById("dropdownMenuButton")
    nodeButton.textContent = node
    localStorage.setItem(uniqueKey("node"), node)

    await setData()
}


async function signMessage() {
    let message = document.getElementById("message")

    let result = (await (await fetch("/sign", {
        method: "POST",
        body: JSON.stringify({message: message.value,
            private_key: localStorage.getItem(uniqueKey("privateKey"))})
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