let worker = null;

function initWorker() {
    worker = new Worker("static/js/update_listener.js");
    worker.addEventListener("message", function (e) {
        const content = e.data[1];
        const error = content["error"];
        if (error !== undefined) {
            throw error;
        }
        const status = content["status"];
        const result = content["result"];
        if (status === "done" && result === undefined) {
            throw new Error("Error: Supplied done status with no result");
        }
        if (status === undefined) {
            throw new Error("Status undefined");
        }
        document.getElementById("status-place").innerText = status;
        if (status === "done") {
            document.getElementById("status-place").classList.add("status-success");
            document.getElementById("status-place").classList.remove("status-error");
            
            document.getElementById("message-holder").hidden = false;
            document.getElementById("message-place").innerText = result;
            worker.terminate();
        }
    });
}

async function formSubmit(e) {
    e.preventDefault();

    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
        return;
    }

    document.getElementById("status-place").innerText = "Loading...";
    document.getElementById("message-holder").hidden = true;
    const file = document.getElementById("image").files[0];
    const lang = document.getElementById("lang").value;

    const result = await uploadFile(file, lang);
    if (!result) {
        throw new Error("Request id cannot be resolved from response");
    }
    try {
        initWorker(); 
    } catch (e) {
         document.getElementById("status-place").innerText = "Error: " + e || e.message + ";";
         document.getElementById("status-place").classList.remove("status-success");
         document.getElementById("status-place").classList.add("status-error");
    }
    worker.postMessage([result["request_id"]]);
}

async function uploadFile(file, lang) {
    return new Promise(
        (resolve, reject) => {
            const timeout = setTimeout(function () {
                didTimeOut = true;
                document.getElementById("message-place").innerText = "Timeout Error.";
                reject(new Error("Request timeout"));
            }, 60000);

            const reader = new FileReader();
            reader.readAsDataURL(file);

            reader.onload = () => {
                const data = reader.result;

                fetch("api/image_submit/", {
                        method: "POST",
                        body: JSON.stringify({"image": data, "lang": lang})
                    }
                )
                    .then(resp => {
                        clearTimeout(timeout);
                        try {
                            const resp_json = resp.json();
                            resolve(resp_json);
                        } catch (e) {
                        }
                    })
                    .catch(x => {
                        document.getElementById("status-place").innerText = "Error: " + resp.status + ";" + resp.text();
                        document.getElementById("status-place").classList.remove("status-success");
                        document.getElementById("status-place").classList.add("status-error");
                    
                        console.exception(e);
                        console.error("Server returned: " + resp.status + "; " + resp.text());
                        reject(x);
                    });
            };
        }
    )
}
