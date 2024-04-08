function confirmSend() {
    $('#confirmModal').modal('show');
}

function sendTransaction() {
    $('#confirmModal').modal('hide');

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


async function setData() {
    let addressText = document.getElementById("address")
    let balanceText = document.getElementById("balance")
    let nodes = document.getElementById("nodes")

    let walletData = await (await fetch("/get_wallet_data")).json()

    addressText.textContent = walletData["address"]
    balanceText.textContent = `${walletData["balance"]} POA`

    for (const node of walletData["nodes"]) {
        nodes.innerHTML += `<a class="dropdown-item" href="#" onclick="setNode(this)">${node}</a>`
    }

    let currentNode = localStorage.getItem("node")
    let nodeButton = document.getElementById("dropdownMenuButton")

    if (currentNode) {
        nodeButton.textContent = currentNode
    } else {
        let randomNode = walletData["nodes"][Math.floor(Math.random() * walletData["nodes"].length)];
        nodeButton.textContent = randomNode
        localStorage.setItem("node", randomNode)
    }
}

async function setNode(node) {
    node = node.innerText
    let nodeButton = document.getElementById("dropdownMenuButton")
    nodeButton.textContent = node
    localStorage.setItem("node", node)
}


async function signMessage() {
    let message = document.getElementById("message")

    let result = (await (await fetch("/sign", {
        method: "POST",
        body: JSON.stringify({message: message.value})
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