let worker = null;

function initWorker() {
    worker = new Worker("static/js/update_listener.js");
    worker.addEventListener("message", function (e) {
        const content = e.data[0];
        $("#message-place").innerText = content;
        worker.terminate();
    });
}

async function formSubmit(e) {
    e.preventDefault();

    const requestId = generateRequestId();

    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
        return;
    }

    const file = document.getElementById("image").files[0];

    await uploadFile(file, requestId);

    initWorker();
    worker.postMessage([requestId]);
    document.getElementById("message-place").innerText = "Loading...";
}

async function uploadFile(file, requestId) {
    return new Promise(
        (resolve, reject) => {
            const reader = new FileReader();
            reader.readAsText(file);

            reader.onload = () => {
                const data = reader.result;

                fetch("/image_submit", {
                        method: "POST",
                        body: JSON.stringify({"image": data})
                    }
                )
                    .then(resp => resp.json())
                    .then(resp => resolve(resp))
                    .catch(x => {
                        reject(x)
                    });
            };
        }
    )
}

function generateRequestId() {
    return "123";
}