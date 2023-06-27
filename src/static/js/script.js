Split(['#split-0', '#split-1'])

let editor = ace.edit("editor");
let Range = ace.require("ace/range").Range;
editor.setTheme("ace/theme/kuroir");
editor.getSession().setMode("ace/mode/yaml");
document.getElementById('editor').style.fontSize='15px';
editor.setOption({
    enableBasicAutocompletion: true,
    fontFamily: "tahoma",
    enableSnippets: true,
    enableLiveAutocompletion: true
});

/**
 * Invoke file input for .yml, .yaml, and .json files
 * If file is input, invoke uploadFile() function
 * 
 * @function
 * @fires uploadFile(event)
 */
function pickFile() {
    const fileInput = document.createElement("input");
    fileInput.id = "fileUpload";
    fileInput.type = "file";
    fileInput.accept = ".yml, .yaml, .json";
    fileInput.onclick = "this.value=null";
    fileInput.addEventListener("change", function(event) {
        uploadFile(event)
    })
    fileInput.click();
}

/**
 * Copies content in .yml, .yaml, or .json file into editor
 * 
 * @function
 * @param {Event} event 
 */
function uploadFile(event) {
    const file = event.target.files[0]
    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            editor.setValue(e.target.result);
        }
        reader.readAsText(file);
    }
}

function saveFile() {
    var textArea = editor.getValue();
    if (textArea == "") {
    alert("Please input an OAS before saving to file!");
    return;
    } else if (fileName = prompt("Save file as", "")) {
    var textBlob = new Blob([textArea], {type:"text/plain"});
    var downloadLink = document.createElement("a");
    downloadLink.download = fileName;
    downloadLink.innerHTML = textBlob;
    if (window.webkitURL != null) { // Chrome
        downloadLink.href = window.webkitURL.createObjectURL(textBlob);
    } else { // Firefox
        downloadLink.href = window.URL.createObjectURL(textBlob);
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }
    downloadLink.click();
    }
}

function loadDictionary() {
    var dictionaryModal = new bootstrap.Modal(document.getElementById("dictionaryModal"));
    var dictionaryTextArea = document.getElementById('customDictionary');
    const file = "static/dictionary/customDictionary.txt" // somehow fetch only works with files in the static folder
    const extension = file.split('.').pop().toLowerCase()
    const allowedExtensions = ['txt', 'csv', 'xlsx']
    if (allowedExtensions.includes(extension)) {
    if (extension == 'txt' || extension == 'csv') {
        fetch(file)
        .then(response => response.text())
        .then(text => {
            dictionaryTextArea.value = text;
        })
        .catch(error => {
            alert("Error in reading .txt/.csv dictionary file")
        })
    } else {
        fetch(file)
        .then(response => response.arrayBuffer())
        .then(buffer => {
            const data = new Uint8Array(buffer)
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const wordsArray = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            
            const formattedText = wordsArray.join("\n")
            dictionaryTextArea.value = formattedText
        })
        .catch(error => {
            alert("Error in reading .xlsx dictionary file")
        })
    }
    } else {
    alert("Wrong dictionary file format. Please try another file.")
    }
}

function addAccordionItem(id, errorLine, errorKeyword, errorMessage, errorAdditionalInfo) {
    var newItemId =  'item' + id + Date.now();

    const br = document.createElement("br");

    var newItem = document.createElement('div');
    newItem.classList.add('accordion-item');
    newItem.setAttribute('style', 'margin-bottom: 10px; border-radius: 5px');

    var newItemHeader = document.createElement('div');
    newItemHeader.classList.add('accordion-header');

    newItemHeader.id = newItemId + '-header';
    var newItemButton = document.createElement('button');
    newItemButton.classList.add('accordion-button');
    newItemButton.classList.add('collapsed');
    newItemButton.setAttribute('type', 'button');
    newItemButton.setAttribute('data-bs-toggle', 'collapse');
    newItemButton.setAttribute('data-bs-target', '#' + newItemId + '-collapse');
    newItemButton.setAttribute('aria-expanded', "false");
    newItemButton.setAttribute('aria-controls', newItemId + '-collapse');
    newItemButton.setAttribute('style', 'margin-bottom: 0; border: 1.5px solid #6f42c1; border-radius: 5px');
    newItemButton.setAttribute('onmouseover', "this.classList.add('hovered')")
    newItemButton.setAttribute('onmouseout', "this.classList.remove('hovered')")
    newItemButton.setAttribute('data-line', errorLine);
    newItemButton.textContent = "Line " + errorLine + " --- " + errorKeyword;

    var newItemCollapse = document.createElement('div');
    newItemCollapse.classList.add('accordion-collapse', 'collapse');
    newItemCollapse.setAttribute('id', newItemId + '-collapse');
    newItemCollapse.setAttribute('aria-labelledby', newItemId + '-header');
    newItemCollapse.setAttribute('data-bs-parent', '#accordion');

    var newItemBody = document.createElement('div');
    newItemBody.classList.add('accordion-body');
    newItemBody.innerHTML += errorAdditionalInfo[0] + ": " + errorAdditionalInfo[1];
    newItemBody.appendChild(br);
    newItemBody.innerHTML += errorMessage; 

    newItemHeader.appendChild(newItemButton);
    newItemCollapse.appendChild(newItemBody);
    newItem.appendChild(newItemHeader);
    newItem.appendChild(newItemCollapse);

    var accordionContainer = document.getElementById('errorPanel');
    accordionContainer.appendChild(newItem); 
}

function refreshAccordion() {
    var accordionContainer = document.getElementById('errorPanel');
    accordionContainer.innerHTML = '';
}

function previewOAS(data) {
    var swaggerUIOptions = {
    dom_id: '#oasPreviewBody', // Determine what element to load swagger ui
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
    ],
    plugins: [
        SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: 'BaseLayout',
    }
    swaggerUIOptions.spec = jsyaml.load(data, {schema:jsyaml.JSON_SCHEMA})
    SwaggerUIBundle(swaggerUIOptions)
}


// =========================================================================================================================

// Real-time side panel refresh after each validation response
// Using debounce to buffer each post request by DEBOUNCE_BUFFER
let debounce;
const DEBOUNCE_BUFFER = 1500;
editor.getSession().on("change", function (e) {
    var editorBorder = document.querySelector('#editor');
    editorBorder.style.border = '2px solid #000';

    clearTimeout(debounce);
    debounce = setTimeout(function extractOAS () {
        var data = editor.getValue();
        if (data.trim() == "" || data == undefined) {
        errorPanel.classList.remove('active');
        previewPanel.classList.remove('active')
        return;
        }

        // Catches one indentation error at a time
        // Make sure user handles all indentation errors before checking OAS
        // Shows and highlights row with indentation errors in editor
        var syntaxErrors = editor.getSession().getAnnotations();
        if (syntaxErrors.length != 0) {
        line = syntaxErrors[0]["row"];
        errorText = syntaxErrors[0]["text"];
        errorType = syntaxErrors[0]["type"];
        editor.gotoLine(line); // thinking about how to improve this
        var highlightRange = new Range(line, 0, line, 300);
        editor.selection.setRange(highlightRange);
        editor.session.addMarker(highlightRange, "error", "text");
        // var customAnnotations = [
        // {
        //   row: line + 5,
        //   column: 0,
        //   text: "test", // or the json reply from the parser
        //   type: "error" // also "warning" and "information"
        // },
        // {
        //   row: line + 10,
        //   column: 0,
        //   text: "test", // or the json reply from the parser
        //   type: "error" // also "warning" and "information"
        // }]
        // editor.getSession().setAnnotations(syntaxErrors.concat(customAnnotations))
        return;
        }

        // console.log(editor.getSession().getAnnotations())
        // editor.session.setOption("useWorker", false) # use when the annotations disappear
        // editor.getSession().setAnnotations([{
        //   row: 1,
        //   column: 0,
        //   text: "test", // or the json reply from the parser
        //   type: "error" // also "warning" and "information"
        // }])

        // editor.session.addMarker(new Range(startRow, startColumn, endRow, endColumn), className, type: ["text", "fullLine", "screenLine"], inFront (opt))

        // var highlightRange = new Range(10, 0, 10, 300);
        // editor.selection.setRange(highlightRange);
        // editor.session.addMarker(highlightRange, "error", "text");

        // editor.getSession().setAnnotations([{
        //     row: 3,
        //     column: 0,
        //     text: "test",
        //     type: "error"
        // }, {
        //     row: 5,
        //     column: 5,
        //     text: "test2",
        //     type: "error"
        // }])

        // console.log(editor.getSession().getAnnotations())


        // console.log(editor.getSession().getValue());
        // session.getLength() --> Gets total number of lines of the yaml file
        // session.getLine(line) --> Gets the string value of the line at line <line>
        // session.getLines(line1, line2) --> Gets the string values of line 1 and line 2 
        // gotoLine(line) --> Scrolls the screen down to line <line>

        

        
        var dictionaryWords = $('#customDictionary').val().split(/\r?\n/);

        $('#loading').show();

        var url = document.location.protocol + "//" + document.location.hostname + ":8080/validate"

        $.ajax({
        data: JSON.stringify({
            doc: data,
            dictionary: dictionaryWords,
        }),
        method: 'POST',
        contentType: 'application/json',
        // url: url, // the browser is unable to resolve service names into IP so if used locally, you can use localhost
        // url: 'http://node:8080/validate',
        success: function(response) {              
            $('#loading').hide();

            previewOAS(data);

            errorPanel.classList.remove('active');
            previewPanel.classList.add('active')
            
            editorBorder.style.border = '2px solid #20c997';
        },
        error: function(response) {
            $('#loading').hide();
            var listErrors = JSON.parse(response["responseText"]) // list of dictionary objects

            refreshAccordion();

            var formattedErrors = []
            for (let i = 0; i < listErrors.length; i++){
            var id = i;
            var errorLine = listErrors[i]["line_number"];
            var errorKeyword = listErrors[i]["keyword"];
            var errorMessage = listErrors[i]["error_message"];
            
            var errorAdditionalInfo = listErrors[i]["params"]
            formattedErrors.push({
                id: id,
                errorLine: errorLine,
                errorKeyword: errorKeyword,
                errorMessage: errorMessage,
                errorAdditionalInfo: errorAdditionalInfo
            })
            }

            formattedErrors.sort((a, b) => a.errorLine - b.errorLine);

            for (var error of formattedErrors) {
            id = error["id"]
            errorLine = error["errorLine"];
            errorKeyword = error["errorKeyword"];
            errorMessage = error["errorMessage"];
            errorAdditionalInfo = Object.entries(error["errorAdditionalInfo"]);
            errorAdditionalInfo = [errorAdditionalInfo[0][0], errorAdditionalInfo[0][1]]
            addAccordionItem(id, errorLine, errorKeyword, errorMessage, errorAdditionalInfo);
            }

            previewPanel.classList.remove('active');
            errorPanel.classList.add('active')
            
            editorBorder.style.border = '2px solid #f00';
        },
        complete: function() {
        }
        });
    }, DEBOUNCE_BUFFER);
});


$('#errorPanel').on('click', '.accordion-button:not(.collapsed)', function() {
    var errorLine = parseInt($(this).data("line")) - 1 // ace editor treats first line as 0
    editor.gotoLine(errorLine);
    var highlightRange = new Range(errorLine, 0, errorLine, 300);
    editor.selection.setRange(highlightRange);
})

const errorPanel = document.getElementById('errorPanel');
const previewPanel = document.getElementById('previewPanel');

loadDictionary();


