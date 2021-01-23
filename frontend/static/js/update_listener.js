let myid = "";

onmessage = function (e) {
    myid = e.data[0];
    listen_for_updates().then(res => postMessage([myid, res]));
};

async function sleep(ms) {
    return new Promise(
        resolve => {
            setTimeout(resolve, ms);
        });
}

async function ajax_update() {
    const resp = await fetch(`/status/?id=${myid}`);
    const jsonResp = await resp.json();
    if (jsonResp["status"] !== "fine") {
        return null;
    }
    return jsonResp["content"];
}

async function listen_for_updates() {
    let checkResult = null;
    while (checkResult === null) {
        await sleep(3000);
        checkResult = await ajax_update();
        if (checkResult)
            return checkResult
    }
}