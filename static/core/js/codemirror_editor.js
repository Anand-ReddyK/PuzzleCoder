document.addEventListener("DOMContentLoaded", function() {
    Split(['#problem-details', '#editor-container'], {
        sizes: [45, 55], /* Adjusted sizes */
        minSize: 200,
        gutterSize: 10,
        cursor: 'col-resize',
    });

    // Initialize CodeMirror editor
    var editor = CodeMirror.fromTextArea(document.getElementById('editor-textarea'), {
        mode: "python",
        lineNumbers: true,
        theme: "material-darker", /* Default theme */
        lineWrapping: true,
        extraKeys: {
            "Ctrl-Space": "autocomplete"
        }
    });


    // Set the height for CodeMirror to avoid horizontal scroll
    editor.setSize("100%", "400px");

    // Ensure line wrapping to prevent horizontal scroll
    editor.getWrapperElement().style.whiteSpace = 'pre-wrap';

    // Handle language change
    document.getElementById('language').addEventListener('change', function() {
        var language = this.value;
        var mode = 'python';
        if (language === 'javascript') mode = 'javascript';
        else if (language === 'java') mode = 'text/x-java';

        editor.setOption('mode', mode);
    });

    // Handle theme change
    document.getElementById('theme').addEventListener('change', function() {
        var theme = this.value;
        editor.setOption('theme', theme);
    });
});