var editor;
// console.log(code_to_load.python);
document.addEventListener("DOMContentLoaded", function() {
    Split(['#problem-details', '#editor-container'], {
        sizes: [45, 55], /* Adjusted sizes */
        minSize: 200,
        gutterSize: 10,
        cursor: 'col-resize',
    });

    // Initialize CodeMirror editor
    editor = CodeMirror.fromTextArea(document.getElementById('editor-textarea'), {
        mode: user_language || "python",
        lineNumbers: true,
        theme: "material-darker", /* Default theme */
        lineWrapping: true,
        extraKeys: {
            "Ctrl-Space": "autocomplete"
        }
    });
    editor.setValue(code_to_load[user_language || "python"]);
    document.getElementById('language').value = user_language || "python";

    // Set the height for CodeMirror to avoid horizontal scroll
    editor.setSize("100%", "400px");

    // Ensure line wrapping to prevent horizontal scroll
    editor.getWrapperElement().style.whiteSpace = 'pre-wrap';

    // Handle language change
    document.getElementById('language').addEventListener('change', function() {
        var language = this.value;
        // var mode = 'python';
        if (language === 'javascript'){
            mode = 'javascript';
            editor.setValue(code_to_load.javascript);
        }
        else if (language === 'java'){
            mode = 'text/x-java';
            editor.setValue(code_to_load.java);
        }
        else if(language === 'python'){
            mode = 'python';
            editor.setValue(code_to_load.python);
        }
        editor.setOption('mode', mode);
    });

    // Handle theme change
    document.getElementById('theme').addEventListener('change', function() {
        var theme = this.value;
        editor.setOption('theme', theme);
    });
});