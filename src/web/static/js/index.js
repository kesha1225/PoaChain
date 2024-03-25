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

    setCookie('privateKey', res["private_key"], 30);
    setCookie('publicKey', res["public_key"], 30);
    setCookie('address', res["address"], 30);
    window.location.replace("/wallet");

}


async function logout() {
    eraseCookie("privateKey")
    eraseCookie("publicKey")
    eraseCookie("address")
    window.location.replace("/");
}


function badLogin() {
    $("#errorPopup").toast('show');
    setTimeout(function () {
        $("#errorPopup").toast('hide');
    }, 2000);
}