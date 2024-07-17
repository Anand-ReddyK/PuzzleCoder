
document.getElementById("btn-run").addEventListener("click", function() {
    var code = editor.getValue();
    var language = document.getElementById("language").value;

    sendCodeToBackend(code, language, type="run-code");
})

document.getElementById("btn-submit").addEventListener("click", function() {
    var code = editor.getValue();
    var language = document.getElementById("language").value;

    sendCodeToBackend(code, language, type="submit-code");
})


function sendCodeToBackend(code, language, type){
    var url = window.location.origin + code_submit_url;
    var data = new URLSearchParams();
    data.append('code', code);
    data.append('language', language);
    data.append('type', type);

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrf_token,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: data
    })
    .then(response => {
        console.log(response.json())
    })
}