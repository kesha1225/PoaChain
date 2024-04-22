if (!sessionStorage.tabId) {
    sessionStorage.tabId = Date.now();
}

function uniqueKey(key) {
    return '_' + key;
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
    localStorage.removeItem(uniqueKey('privateKey'))
    localStorage.removeItem(uniqueKey('publicKey'))
    localStorage.removeItem(uniqueKey('address'))
    window.location.replace("/");
}

async function toBlocks() {
    window.location.replace("/blocks");
}

async function toMain() {
    window.location.replace("/wallet");
}


function badLogin() {
    $("#errorPopup").toast('show');
    setTimeout(function () {
        $("#errorPopup").toast('hide');
    }, 2000);
}

function onloadAdaptive() {
    if (window.innerWidth < 900) {
        document.getElementById("logoIMG").hidden = true
        document.getElementById("setAllBTN").className = "btn btn-secondary btn-sm"
        document.getElementById("sendlink").className = "nav-link active btn-sm"
        document.getElementById("signlink").className = "nav-link btn-sm"

        document.getElementById("allTrans").className = "nav-link active btn-sm"
        document.getElementById("receive").className = "nav-link btn-sm"
        document.getElementById("sent").className = "nav-link btn-sm"


    }
}


function timeConverter(UNIX_timestamp) {
    let a = new Date(UNIX_timestamp / 1000);
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    let year = a.getFullYear();
    let month = months[a.getMonth()];
    let date = a.getDate();
    let hour = a.getHours();
    let min = a.getMinutes();
    let sec = a.getSeconds();
    let time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
    return time;
}