//======================= Dependencies =================================================
const Ajv = require("ajv");
const AjvErrors = require("ajv-errors");
const AjvKeywords = require("ajv-keywords");
const addFormats = require("ajv-formats");

const yaml = require("js-yaml");

const fs = require("fs");

const _ = require("lodash");

const SpellChecker = require('spellchecker');

const WordsNinjaPack = require('wordsninja');
const WordsNinja = new WordsNinjaPack();

const natural = require('natural');
const tokenizer = new natural.WordTokenizer();

const http = require('http');
const path = require("path");

//======================= Utils =================================================

// customDict is an array of words specific to the CPF context
var customDict = []

async function fetchLineNumber(doc, pathArray) {
  // Uses Fetch API to call our function from Flask server to get line number based on ruamel.yaml number line mapping
  // To simplify line number mapping. If there's a simpler way to do this on JS, this can be deprecated
  // WARNING: Fetch API in experimental-mode 
  try {
    // const response = await fetch("http://127.0.0.1:80/getLineNumber", {
    const response = await fetch("http://flask:443/getLineNumber", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        docString: doc,
        pathArray: pathArray
      })
    });

    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Request failed with status ' + response.status);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

function getPathSegments(path) {
  var pathSegments = path.split("/")
  var pathVersionAt = -1
  if (pathSegments.length == 4) {
    pathVersionAt = 2
  }
  else if (pathSegments.length == 5) {
    pathVersionAt = 3
  }
  else if (pathSegments.length == 6) {
    pathVersionAt = 4
  }
  const leftSlice = pathSegments.slice(1, pathVersionAt)
  const rightSlice = pathSegments.slice(pathVersionAt + 1)
  pathSegments = [...leftSlice, ...rightSlice]

  return pathSegments
}

// WordsNinja do not allow adding custom words during runtime or it is too expensive
// Faster (maybe) to check it with our own list
// Even faster if pre-processing is doen to the list before searching
function wordInCustomDict(word) {
  for (var customWord of customDict) {
    if (word.toLowerCase() == customWord.toLowerCase()) {
      return true
    }
  }
  return false
}

//======================= Ajv Setup =================================================
const ajv = new Ajv({
  schemaId: "id",
  allErrors: true,
})
addFormats(ajv, ["uri-reference", "email", "regex", "uri"])
AjvErrors(ajv) // add all ajv-errors keywords, significantly, errorMessage
require("ajv-keywords")(ajv) // add all ajv-keywords keywords

// ===================== Custom Validation Rules ====================================
// Rules following CPFB API Standards v1.1.2

// keywords should be delimited by "-" to avoid future name collisions
ajv.addKeyword({
    keyword: "path-characters", 
    validate: function checkPathCharacters(schema, data, parentSchema, dataPath)  {
      // Checks for special characters in path, except for "/"
      if (schema == false) {
        return true
      }
      const path = dataPath["parentDataProperty"]
      const regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>? ]/
      if (regex.test(path)) {
        checkPathCharacters.errors = [
          {
            keyword: "path-characters",
            message: "Special characters in path not allowed",
            params: {
              pathCharacters: false
            }
          }
        ]
        return false
      }
      return true
    }
})
// Internal API Route format: /<API Product>/<Subtier 1>/<Subtier 2>/<VersionNum>/<Verb>
// Subtiers are optional
// TODO: Check camelCase of properties
ajv.addKeyword({ 
    keyword: "path-length",
    validate: function checkPathLength(schema, data, parentSchema, dataPath) {
      // Checks if the path length is 4, 5, or 6
      if (schema == false) {
        return true
      }
      const path = dataPath["parentDataProperty"]
      const pathSegments = path.split("/")
      if (pathSegments.length == 4 || pathSegments.length == 5 || pathSegments.length == 6) {
        return true
      }
      checkPathLength.errors = [
        {
          keyword: "path-length",
          message: "Invalid path length.",
          params: {
            pathLength: false
          }
        }
      ]
      return false
    }
})
ajv.addKeyword({
  keyword: "api-product",
  validate: function checkAPIProduct(schema, data, parentSchema, dataPath) {
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    const pathSegments = path.split("/")
    const apiProduct = pathSegments[1]
    const allowedAPIProducts = [ // hardcoded here, would be better if there is a central repository with this information to extract at runtime
                                "accountClosure", "adjustment", "agencyCommon", "agencyPortal", "ariseCommon", 
                                "businessProcessAutomation", "careshieldCustomerService", "careshieldEService", "corporateServices", "cpfLife",
                                "customerEngagement", "dataServices", "digitalServices", "discretionaryWithdrawals", "matrimonialAssetDivision",
                                "education", "employerContribution", "employerEnforcement", "employerEServices", "familyProtection",
                                "finance", "healthcareCommon", "healthcareGrants", "housing", "housingMonetisation",
                                "humanResources", "idAccessManagement", "investment", "assetManagement", "resourceManagement",
                                "longTermCareInsurance", "matchedRetirementSavings", "medicalInsurance", "medisave", "mediasaveCare",
                                "memberAccounts", "memberRecords", "memberSystemsCommon", "niceCustomerManagement", "nomination",
                                "procurement", "receiptAndPayment", "retirementTopUp", "retirement", "selfEmployedContribution",
                                "selfEmployedEnforcement", "silverSupport", "surplusSupport", "voluntaryContribution", "corporateDesktop",
                                "wordfare"
                              ]
    if (!allowedAPIProducts.includes(apiProduct)) { 
      checkAPIProduct.errors = [
        {
          keyword: "api-product",
          message: "Invalid API Product.",
          params: {
            apiProduct: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "path-version",
  validate: function checkPathVersion(schema, data, parentSchema, dataPath) {
    // Checks for path version in path
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    const pathSegments = path.split("/")
    var pathVersion = null
    if (pathSegments.length == 4) {
      pathVersion = pathSegments[2]
    }
    else if (pathSegments.length == 5) {
      pathVersion = pathSegments[3]
    }
    else if (pathSegments.length == 6) {
      pathVersion = pathSegments[4]
    }
    const regex = /^[vV]\d+$/
    if (pathVersion == "" || pathVersion == null || !regex.test(pathVersion)) {
      checkPathVersion.errors = [
        {
          keyword: "path-version",
          message: "Invalid or missing path version",
          params: {
            pathVersion: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "match-version",
  validate: function checkMatchingVersion(schema, data, parentSchema, dataPath) {
    // Check if the version in path matches the version in <Info>
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    const pathSegments = path.split("/")
    var pathVersion = null
    if (pathSegments.length == 4) {
      pathVersion = pathSegments[2]
    }
    else if (pathSegments.length == 5) {
      pathVersion = pathSegments[3]
    }
    else if (pathSegments.length == 6) {
      pathVersion = pathSegments[4]
    }
    const pathVersionNum = parseInt(pathVersion.substring(1))
  
    var infoVersionNum = -1
    try {
      infoVersionNum = dataPath["rootData"]["info"]["version"][0] 
    } catch (error) {
      checkMatchingVersion.errors = [
        {
          keyword: "match-version",
          message: "Missing version in [Info]",
          params: {
            matchVersion: false
          }
        }
      ]
      return false
    }
  
    if (pathVersionNum != infoVersionNum) {
      checkMatchingVersion.errors = [
        {
          keyword: "match-version",
          message: "Version in path does not match with version in [info]",
          params: {
            matchVersion: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "camel-casing",
  validate: function checkCamelCasing(schema, data, parentSchema, dataPath) {
    // Checks if the path segment is in camel casing format
    // Warning: Compound words not handled
    if (schema == false) {
      return true
    }
    const pathSegmentsNotCamelCase = []
    const path = dataPath["parentDataProperty"]
    var pathSegments = getPathSegments(path)
    for (var segment of pathSegments) {
      var words = _.words(segment) // splits subtier into words using lodash based on camel casing
      for (var word of words) {
        if (SpellChecker.isMisspelled(word) && !wordInCustomDict(word)) {
          subtiersNotCamelCase.push(segment)
          break
        }
      }
    }
    if (pathSegmentsNotCamelCase.length != 0) {
      const pathSegmentsNotCamelCase_string = pathSegmentsNotCamelCase.join(', ')
      checkCamelCasing.errors = [
        {
          keyword: "camel-casing",
          message: `The following segments(s) are not in camel case format: "${pathSegmentsNotCamelCase_string}"`,
          params: {
            camelCasing: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "path-spelling",
  validate: function checkPathSpelling(schema, data, parentSchema, dataPath) {
    // Checks the spelling of all words in segments (because spelling-check does not apply to concatenated strings)
    // Warning: Compounds words not handled
    // Will not send info on words to correct because behaviour of WordsNinja not stable; possible if it separates words better
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    var pathSegments = getPathSegments(path)
    const segmentsSpelledWrongly = []
    for (var segment of pathSegments) {
      var words = WordsNinja.splitSentence(segment) // split words using Wordsninja based on word identification
      for (var word of words) {
        if (SpellChecker.isMisspelled(word) && !wordInCustomDict(word)) {
          subtiersSpelledWrongly.push(segment)
          break
        }
      }
    }
    if (segmentsSpelledWrongly.length != 0) {
      const segmentsSpelledWrongly_string = segmentsSpelledWrongly.join(", ")
      checkPathSpelling.errors = [
        {
          keyword: "path-spelling",
          message: `One or more words in the following subtier(s) are not spelled correctly: "${segmentsSpelledWrongly_string}"`,
          params: {
            pathSpelling: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({ 
  keyword: "path-verb",
  validate: function checkVerb(schema, data, parentSchema, dataPath) {
    // Checks if the first word of the Verb is a verb
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    var pathSegments = path.split("/")
    const pathVerb = pathSegments[pathSegments.length - 1]

    const allowedVerbs = ["create", "get", "update", "delete", "compute", "transact", "check", "transfer"]

    var words = _.words(pathVerb)
    var verb = words[0]
    if (!allowedVerbs.includes(verb)) {
      checkVerb.errors = [
        {
          keyword: "path-verb",
          message: `The word "${verb}" in "${pathVerb}" is not a valid verb in the API Standards.`,
          params: {
            subtierVerb: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "required-properties",
  validate: function checkProperties(schema, data, parentSchema, dataPath) {
    // Checks if elements in <required> are present in <properties>
    if (schema == false) {
      return true
    }
    const propertiesNotPresent = [] // duplicate properties already handled in schema
    const parentData = dataPath["parentData"]
    const propertiesList = Object.keys(parentData["properties"])
    const requiredList = parentData["required"]
    for (var requiredProperty of requiredList) {
      if (!propertiesList.includes(requiredProperty)) {
        propertiesNotPresent.push(requiredProperty)
      }
    }
    if (propertiesNotPresent.length > 0) {
      const propertiesNotPresent_string = propertiesNotPresent.join(", ")
      checkProperties.errors = [
        {
          keyword: "required-properties",
          message: `The following properties are not present: ${propertiesNotPresent_string} `,
          params: {
            requiredProperties: false
          }
        }
      ]
      return false
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "spelling-check",
  validate: function checkSpelling(schema, data, parentSchema, dataPath) {
    // Spelling checking feature
    // Mainly used on descriptions and titles and excludes extensions (e.g., x-author)
    // Open for improvement
    if (schema == false) {
      return true
    }
    const words = tokenizer.tokenize(data)
    var wordsSpelledWrong = new Set()
    for (var word of words) {
      if (SpellChecker.isMisspelled(word) && !wordInCustomDict(word)) {
        wordsSpelledWrong.add(word)
      }
    }
    if (wordsSpelledWrong.size != 0) {
      var formattedWordsSpelledWrong = ''
      wordsSpelledWrong.forEach(word => {formattedWordsSpelledWrong += `- ${word} ==> ${SpellChecker.getCorrectionsForMisspelling(word).join(", ")}<br>`})
      var errorMessage = 'The following word(s) are spelled incorrectly in this field:' + '<br>' + formattedWordsSpelledWrong
      checkSpelling.errors = [
        {
          keyword: 'spelling-check',
          message: errorMessage,
          params: {
            checkSpelling: false
          }
        }
      ]
      return false
    }
    return true
  }
})

async function validateYAML(doc, dictionary) { 
  await WordsNinja.loadDictionary(); // forced async function by WordsNinja library
  customDict = dictionary; // global dictionary in this file

  var validate = false
  try {
    const schema_string = fs.readFileSync('oas3.0_schema.yaml', 'utf-8')
    const schema = yaml.load(schema_string)
    validate = ajv.compile(schema)
  }
  catch {
    return null
  }

  // const data_string = fs.readFileSync('examples/example1.yaml', 'utf-8')
  var data = null
  try {
    data = yaml.load(doc)
  } catch (error) {
    return null
  }
  
  var payload = []
  if (!validate(data)) {
    for (var error of validate.errors) {
      // ignore if/then/else errors because we created more useful error messages
      if (["if", "then", "else"].includes(error["keyword"])) {
        continue;
      }
      var path = error["instancePath"]
      var pathArray = path.split("/").slice(1,)
      // change back "/" that are converted from ajv
      for (var j = 0; j < pathArray.length; j++) {
        if (pathArray[j]) {
          pathArray[j] = pathArray[j].replace(/~1/g, "/")
        }
      }
      var line = -1;
      
      // get line number, error message, instance path, and schema path
      await fetchLineNumber(doc, pathArray)
        .then((data) => {
          line = data["lineNumber"]
        })
        .catch((error) => {
          return null
        })
      payload.push({
        line_number: line,
        keyword: error.keyword,
        error_message: error.message[0].charAt(0).toUpperCase() + error.message.slice(1) ,
        params: error.params
      })
    }
  }
  return payload
}

//==================== Server ===================================

const hostname = '0.0.0.0'; 
const port = 80; 

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*'); // Allow requests from any origin
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'); // Specify the allowed HTTP methods
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type'); // Specify the allowed headers

  if (req.method === 'OPTIONS') {
    // Handle preflight OPTIONS request
    res.statusCode = 204; // No content needed for preflight
    res.end();
    return;
  }

  if (req.url == '/validate' && req.method === 'POST') {
    let requestBody = ''
    req.on('data', (chunk) => {
      requestBody += chunk
    })
    req.on('end', async () => {
      try {
        const jsonData = JSON.parse(requestBody)
        var payload = await validateYAML(jsonData["doc"], jsonData["dictionary"])
        if (payload == null) { // unexpected error
          res.statusCode = 204;
          res.setHeader('Content-Type', 'text/html');
          res.write("Unexpected error!")
          res.end();
        }
        else if (payload.length == 0) { // successful yaml doc
          res.statusCode = 200;
          res.setHeader('Content-Type', 'text/html');
          res.write("Successful!")
          res.end();
        }
        else { // unsuccessful yaml doc
          res.statusCode = 400;
          res.setHeader('Content-Type', 'text/html');
          res.write(JSON.stringify(payload))
          res.end();
        }
      } catch (error) {
        res.statusCode = 405;
        res.end();
      }
    })
  }
  else {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'text/plain');
    res.write("404 Page Not Found")
    res.end();
  }
  
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});