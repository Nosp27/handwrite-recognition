let myid = "";

onmessage = function (e) {
    myid = e.data[0];
    listen_for_updates();
};

async function sleep(ms) {
    return new Promise(
        resolve => {
            setTimeout(resolve, ms);
        });
}

async function ajax_update() {
    const resp = await fetch(`/api/status/?request_id=${myid}`);
    if (resp.status === 200)
        return await resp.json();
    throw new Error("Server returned " + resp.status);
}

async function listen_for_updates() {
    let checkResult = {"status": ""};
    while (checkResult["status"] !== "done") {
        await sleep(3000);
        try {
            checkResult = await ajax_update();
        }
        catch (err) {
            checkResult = {"status": "unknown", "error": err.toString()}
        }
        postMessage([myid, checkResult]);
    }
}
