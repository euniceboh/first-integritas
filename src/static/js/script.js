// const express_url = "http://localhost:3000/validate" // local
const express_url = process.env.nodeUrl // pipeline
// const express_url = "https://cpfdevportal-node.azurewebsites.net/validate" // pipeline

/**
 * Startup
 */
$(document).ready(function() {
    // Init for SplitJS
    Split(['#split-0', '#split-1'])

    // Ace Editor Configs
    let editor = ace.edit("editor");
    editor.setTheme("ace/theme/kuroir");
    editor.getSession().setMode("ace/mode/yaml"); 
    document.getElementById('editor').style.fontSize='15px';
    editor.setOption({
        enableBasicAutocompletion: true,
        fontFamily: "tahoma",
        enableSnippets: true,
        enableLiveAutocompletion: true
    })

    loadDictionary();
})

/**
 * Invoke file input for YAML/JSON files
 * If file is input, invoke uploadFile() function
 * YAML/JSON file formats allowed: .yml, .yaml, .json
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
 * Copies content in selected file into editor
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

/**
 *  Prompts the user for a file name and saves the contents of the editor to a file
 *  File is downloaded locally
 * 
 * @function 
 */
function saveFile() {
    let textArea = editor.getValue();
    if (textArea == "") {
        alert("Please input an OAS before saving to file!");
    } else {
        let fileName = prompt("Save file as", "")
        if (fileName) {
            let textBlob = new Blob([textArea], {type:"text/plain"});
            let downloadLink = document.createElement("a");
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
}

/**
 * Loads the dictionary file from path specified into dictionary textarea element
 * Dictionary file formats allowed: .txt, .csv, .xlsx
 * 
 * @function
 */
function loadDictionary() {
    let dictionaryTextArea = document.getElementById('customDictionary');
    const file = "static/dictionary/customDictionary.txt"
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

/**
 * Adds accordion item per error detected into error panel
 * 
 * @function
 * @param {number} id 
 * @param {string} errorLine 
 * @param {string} errorKeyword 
 * @param {string} errorMessage 
 * @param {List} errorAdditionalInfo
 */
function addAccordionItem(id, errorLine, errorKeyword, errorMessage, errorAdditionalInfo) {
    let newItemId =  'item' + id + Date.now();

    const br = document.createElement("br");

    let newItem = document.createElement('div');
    newItem.classList.add('accordion-item');
    newItem.setAttribute('style', 'margin-bottom: 10px; border-radius: 5px');

    let newItemHeader = document.createElement('div');
    newItemHeader.classList.add('accordion-header');

    newItemHeader.id = newItemId + '-header';
    let newItemButton = document.createElement('button');
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

    let newItemCollapse = document.createElement('div');
    newItemCollapse.classList.add('accordion-collapse', 'collapse');
    newItemCollapse.setAttribute('id', newItemId + '-collapse');
    newItemCollapse.setAttribute('aria-labelledby', newItemId + '-header');
    newItemCollapse.setAttribute('data-bs-parent', '#accordion');

    let newItemBody = document.createElement('div');
    newItemBody.classList.add('accordion-body');
    newItemBody.innerHTML += errorAdditionalInfo[0] + ": " + errorAdditionalInfo[1];
    newItemBody.appendChild(br);
    newItemBody.innerHTML += errorMessage; 

    newItemHeader.appendChild(newItemButton);
    newItemCollapse.appendChild(newItemBody);
    newItem.appendChild(newItemHeader);
    newItem.appendChild(newItemCollapse);

    let accordionContainer = document.getElementById('errorPanel');
    accordionContainer.appendChild(newItem); 
}

/**
 * Erases all accordions
 * 
 * @function
 */
function refreshAccordion() {
    let accordionContainer = document.getElementById('errorPanel');
    accordionContainer.innerHTML = '';
}


/**
 * Uses SwaggerHub OAS Preview plugin to display API preview of YAML/JSON document
 * 
 * @function
 * @param {string} data 
 */
function previewOAS(data) {
    let swaggerUIOptions = {
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

let debounce
const DEBOUNCE_BUFFER = 1500;
const editor = ace.edit("editor");
editor.getSession().on("change", function (e) {
    // Editor border changes colour to black while the user is editing
    let editorBorder = document.querySelector('#editor');
    editorBorder.style.border = '2px solid #000';

    // Real-time error & preview panel refresh after each validation response
    // Using debounce to buffer each post request by DEBOUNCE_BUFFER
    clearTimeout(debounce);
    debounce = setTimeout(function extractOAS () {
        let docString = editor.getValue()
        if (docString.trim() == "" || docString == undefined) { // empty error/preview panel if editor empty
            errorPanel.classList.remove('active')
            previewPanel.classList.remove('active')
            return;
        }

        // Editor checks for syntax error in YAML/JSON document before validation
        let syntaxErrors = editor.getSession().getAnnotations();
        let Range = ace.require("ace/range").Range;
        if (syntaxErrors != undefined && syntaxErrors.length != 0) {
            let line = syntaxErrors[0]["row"];
            let errorText = syntaxErrors[0]["text"];
            let errorType = syntaxErrors[0]["type"];
            editor.gotoLine(line);
            let highlightRange = new Range(line, 0, line, 300);
            editor.selection.setRange(highlightRange);
            editor.session.addMarker(highlightRange, "error", "text");

            errorPanel.classList.remove('active');
            previewPanel.classList.remove('active')
            return;
        }
        
        // Prepare custom dictionary words into array
        let dictionaryArray = $('#customDictionary').val().split(/\r?\n/);

        $('#loading').show();


        // Invoke validation logic
        fetch(express_url, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                doc: docString,
                dictionary: dictionaryArray
            })
        })
            .then(async response => {
                if (response.status === 204) { // successful YAML/JSON document
                    previewOAS(docString);

                    errorPanel.classList.remove('active');
                    previewPanel.classList.add('active')
                    
                    // Editor border turns green if no errors
                    editorBorder.style.border = '2px solid #20c997';

                    $('#loading').hide();
                } else if (response.status === 200) { // unsuccessful YAML/JSON document
                    let listErrors = await response.json()

                    refreshAccordion();

                    let formattedErrors = []
                    for (let i = 0; i < listErrors.length; i++){
                        let id = i;
                        let errorLine = listErrors[i]["line_number"];
                        let errorKeyword = listErrors[i]["keyword"];
                        let errorMessage = listErrors[i]["error_message"];
                        
                        let errorAdditionalInfo = listErrors[i]["params"]
                        formattedErrors.push({
                            id: id,
                            errorLine: errorLine,
                            errorKeyword: errorKeyword,
                            errorMessage: errorMessage,
                            errorAdditionalInfo: errorAdditionalInfo
                        })
                    }

                    formattedErrors.sort((a, b) => a.errorLine - b.errorLine);

                    for (let error of formattedErrors) {
                        let id = error["id"]
                        let errorLine = error["errorLine"];
                        let errorKeyword = error["errorKeyword"];
                        let errorMessage = error["errorMessage"];
                        let errorAdditionalInfo = Object.entries(error["errorAdditionalInfo"]);
                        errorAdditionalInfo = [errorAdditionalInfo[0][0], errorAdditionalInfo[0][1]]
                        addAccordionItem(id, errorLine, errorKeyword, errorMessage, errorAdditionalInfo);
                    }

                    previewPanel.classList.remove('active');
                    errorPanel.classList.add('active');
                    
                    // Editor border turns red if there are errors
                    editorBorder.style.border = '2px solid #f00';

                    $('#loading').hide();
                } else if (response.status === 500) { // unexpected error with logic
                    throw new Error(response.json().msg)
                } else {
                    throw new Error("Unexpected status code: " + response.status)
                }
            })
            .catch(error => { // cannot communicate with backend
                alert("An unexpected error has occurred reaching the backend server.")
            })

    }, DEBOUNCE_BUFFER);
});

/**
 * Accordion Item onclick event
 */
$('#errorPanel').on('click', '.accordion-button:not(.collapsed)', function() {
    const Range = ace.require("ace/range").Range;
    let errorLine = parseInt($(this).data("line")) - 1
    editor.gotoLine(errorLine);
    let highlightRange = new Range(errorLine, 0, errorLine, 300);
    editor.selection.setRange(highlightRange);
})