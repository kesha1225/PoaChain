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

        document.getElementById("bigScreenP").hidden = true
    }
}


function timeConverter(UNIX_timestamp) {
    let a = new Date(UNIX_timestamp / 1000);
    let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    let year = a.getFullYear();
    let month = months[a.getMonth()];
    let date = a.getDate();
    let hour = a.getHours().toString();
    if (hour.length < 2){
        hour = "0" + hour
    }
    let min = a.getMinutes().toString();
    if (min.length < 2){
        min = "0" + min
    }
    let sec = a.getSeconds().toString();
    if (sec.length < 2){
        sec = "0" + sec
    }
    let time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
    return time;
}

function createTransaction(transaction) {
    let arrow = "&larr;"
    let amount = `-${transaction['amount'] / 100} POA`
    let address = truncateAddress(transaction['recipient_address'], 10)
    let fullAddress = transaction['recipient_address']
    let arrowClass = "red-arrow"
    if (transaction["is_income"]) {
        arrow = "&rarr;"
        amount = `+${transaction['amount'] / 100} POA`
        address = truncateAddress(transaction["sender_address"], 10)
        fullAddress = transaction['sender_address']
        arrowClass = "green-arrow"
    }

    let code = `<div class="card mb-1">
            <div class="card-body">
                <div class="container">
                    <div class="row mb-2">
                        <p class="card-text">
                            <span class="transaction-type-arrow ${arrowClass}">${arrow}</span>
                            <span class="transaction-amount">${amount}</span>
                        </p>
                    </div>
                    <div class="row mb-2">
                        <p class="card-text">
                            <span class="transaction-address">
                            <a style="color: white" href="/address/${fullAddress}">Адрес: ${address}</a>
                            </span>
                    
                        </p>
                    </div>
                    <div class="row mb-2">
                        <p class="card-text transaction-date">${timeConverter(transaction['timestamp'])}</p>
                    </div>
                    <div class="row">
                        <p class="card-text"><button
                         class="btn-sm btn-primary">
                         <a style="color: white"
                         href="/transaction/${transaction['transaction_hash']}">
                         Перейти к транзакции</a></button></p>
                    </div>
                </div>
            </div>

        </div>`

    const newTrans = document.createElement('div');
    newTrans.class = "card mb-1"
    newTrans.innerHTML = code
    return newTrans
}

function truncateAddress(address) {
    return address.substring(0, 5) + '...' + address.substring(address.length - 7, address.length);
}