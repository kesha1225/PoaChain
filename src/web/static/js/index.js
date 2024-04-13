if (!sessionStorage.tabId) {
    sessionStorage.tabId = Date.now();
}
function uniqueKey(key) {
    console.log(sessionStorage.tabId)
    return sessionStorage.tabId + '_' + key;
}

async function createNew() {
    let mnemonicInput = document.getElementById("mnemonic")
    let mnemonicInputLabel = document.getElementById("mnemid")

    mnemonicInput.value = (await (await fetch("/new_mnemonic")).json())["mnemonic"]
    mnemonicInputLabel.textContent = "Сохраните сгенерированную мнемоническую фразу:"
}

async function login() {
    let mnemonicInput = document.getElementById("mnemonic").value.trim()
    let res = await fetch("/get_data_from_mnemonic",
        {
            method: 'POST', headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({mnemonic: mnemonicInput})
        })

    res = await res.json()

    if (!res["ok"]) {
        badLogin()
        return
    }
    res = res["wallet_data"]

    localStorage.setItem(uniqueKey('privateKey'), res["private_key"]);
    localStorage.setItem(uniqueKey('publicKey'), res["public_key"]);
    localStorage.setItem(uniqueKey('address'), res["address"]);
    window.location.replace("/wallet");

}


async function logout() {
    localStorage.clear()
    window.location.replace("/");
}


function badLogin() {
    $("#errorPopup").toast('show');
    setTimeout(function () {
        $("#errorPopup").toast('hide');
    }, 2000);
}