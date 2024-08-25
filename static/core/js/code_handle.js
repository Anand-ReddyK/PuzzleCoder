var run_button = document.getElementById("btn-run");
run_button.addEventListener("click", function() {
    var code = editor.getValue();
    var language = document.getElementById("language").value;

    sendCodeToBackend(code, language, type="run-code");
})

var submit_button = document.getElementById("btn-submit");
submit_button.addEventListener("click", function() {
    var code = editor.getValue();
    var language = document.getElementById("language").value;

    sendCodeToBackend(code, language, type="submit-code");
})


function sendCodeToBackend(code, language, type){
    toggleButtons();
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
    .then(response => response.json())
    .then(data => {
        if (data.message == "Code Enqued"){
            checkResult();
        }
    })

    .catch(error => {
        toggleButtons();
    });
}


function checkResult(){
    fetch(code_result_url, {
        method: "GET"
    })

    .then(response => response.json())
    .then(data => {
        if (data.result !== "Pending"){
            console.log(data.result);
            displayTestResults(data.result);
            toggleButtons();
        }
        else{
            console.log("Checking again...");
            setTimeout(checkResult, 2000);
        }
    })

    .catch(error => {
        toggleButtons();
    });
}

function displayTestResults(data) {
    const terminalOutput = document.getElementById("output");
    terminalOutput.innerHTML = "<h4 class='text-lg font-bold mb-4'>Test Case Results:</h4>";

    data.results.forEach((result, index) => {
        let status = result.passed ? "Passed" : "Failed";
        let statusColor = result.passed ? "bg-green-600" : "bg-red-600";
        let borderColor = result.passed ? "border-green-500" : "border-red-500";

        terminalOutput.innerHTML += `
            <div class="mb-4 p-4 rounded-lg border ${borderColor} bg-gray-800">
                <div class="flex justify-between mb-2">
                    <span class="font-semibold">Test Case ${index + 1}</span>
                    <span class="px-2 py-1 rounded text-white ${statusColor}">${status}</span>
                </div>
                <div class="text-sm">
                    <p><strong>Input:</strong> <code class="bg-gray-700 p-1 rounded">${result.input}</code></p>
                    <p><strong>Expected Output:</strong> <code class="bg-gray-700 p-1 rounded">${result.expected_output}</code></p>
                    <p><strong>Actual Output:</strong> <code class="bg-gray-700 p-1 rounded">${result.actual_output}</code></p>
                </div>
            </div>
        `;
    });

    terminalOutput.innerHTML += `
        <div class="mt-6 p-4 rounded-lg bg-gray-800 border border-gray-700">
            <strong class="text-lg">Pass Rate:</strong> <span class="text-blue-400">${(data.pass_rate * 100).toFixed(2)}%</span>
        </div>
    `;
}

function toggleButtons(){
    if (run_button.disabled == true || submit_button.disabled == true){
        run_button.disabled = false;
        run_button.style.backgroundColor = "#10b981"
        
        submit_button.disabled = false;
        submit_button.style.backgroundColor = "#3b82f6"
    }
    else{
        run_button.disabled = true;
        run_button.style.backgroundColor = "#0e6145"
        
        submit_button.disabled = true;
        submit_button.style.backgroundColor = "#204787"
    }
}