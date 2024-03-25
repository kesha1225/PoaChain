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

    let walletData = await (await fetch("/get_wallet_data")).json()

    addressText.textContent = walletData["address"]
    balanceText.textContent = `${walletData["balance"]} POA`
}