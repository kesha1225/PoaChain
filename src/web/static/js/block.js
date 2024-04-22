let updateAllBlocks = window.setInterval(async function () {
    await blocksLoad()
}, 3000);

let oldHashesBlocks = []

async function blocksLoad() {
    let currentNode = localStorage.getItem(uniqueKey("node"))

    let blocksData = await fetch("/blocks_latest",
        {
            method: 'POST', headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                node: currentNode,
            })
        })

    blocksData = (await blocksData.json())["blocks"]

    let blocksObject = document.getElementById("blockTable")
    for (let block of blocksData) {
        if (oldHashesBlocks.includes(block['block_hash'])){
            continue
        }

        let code = `
            <th scope="row">${block['block_number']}</th>
            <td>${block['authority_id']}</td>
            <td>${timeConverter(block['timestamp'])}</td>
            <td>${block['block_hash']}</td>`
        let newBlock = document.createElement('tr');
        newBlock.innerHTML = code
        blocksObject.prepend(newBlock)
        oldHashesBlocks.push(block['block_hash'])
    }
}