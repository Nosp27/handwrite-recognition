let worker = null;

function initWorker() {
    worker = new Worker("static/js/update_listener.js");
    worker.addEventListener("message", function (e) {
        const content = e.data[1];
        console.log("Update status: " + content);
        document.getElementById("message-place").innerText = content;
        worker.terminate();
    });
}

async function formSubmit(e) {
    e.preventDefault();

    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
        return;
    }

    const file = document.getElementById("image").files[0];
    const lang = document.getElementById("lang").value;
    
    document.getElementById("message-place").innerText = "Loading...";
    const result = await uploadFile(file, lang);
    if (!result) {
        throw new Error("Request id cannot be resolved from response");
    }

    initWorker();
    worker.postMessage([result["request_id"]]);
}

async function uploadFile(file, lang) {
    return new Promise(
        (resolve, reject) => {
            const timeout = setTimeout(function(){
                didTimeOut=true;
                document.getElementById("message-place").innerText = "Timeout Error.";
                reject(new Error("Request timeout"));
            }, 60000);

            const reader = new FileReader();
            reader.readAsText(file);

            reader.onload = () => {
                const data = reader.result;

                fetch("api/image_submit/", {
                        method: "POST",
                        body: JSON.stringify({"image": data, "lang": lang})
                    }
                )
                    .then(resp => {
                        clearTimeout(timeout);
                        const resp_json = resp.json();
                        resolve(resp_json);
                    })
                    .catch(x => {
                        reject(x);
                    });
            };
        }
    )
}
