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
    const resp = await fetch(`/api/status/?request_id=${myid}`);
    const jsonResp = await resp.json();
    if (jsonResp["result"] !== undefined)
        return jsonResp["result"];
    return jsonResp["status"];
}

async function listen_for_updates() {
    let checkResult = "";
    while (checkResult !== "done") {
        await sleep(3000);
        try {
            checkResult = await ajax_update();
            console.log(checkResult);
            if (checkResult)
                return checkResult
        }
        catch (err) {
            console.error(`Could not load status. (id=${myid})`, err);
        }
    }
}
