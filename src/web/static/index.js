

async function createNew(){
    let mnemonicInput = document.getElementById("mnemonic")
    let mnemonicInputLabel = document.getElementById("mnemid")

    console.log(mnemonicInput.value)
    mnemonicInput.value = "fdsfsd fdsfsd fsd fds f sd f sf sd fsdf sdfdsf ds f dsf sd fsdfds"
    mnemonicInputLabel.textContent = "Сохраните сгенерированную мнемоническую фразу:"
}