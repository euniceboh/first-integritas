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
const language = "EN"
const defaultCategory = 'N';
const defaultCategoryCapitalized = 'NNP';
var lexicon = new natural.Lexicon(language, defaultCategory, defaultCategoryCapitalized);
var ruleSet = new natural.RuleSet('EN');
var tagger = new natural.BrillPOSTagger(lexicon, ruleSet);

const http = require('http');

//======================= Utils =================================================

// customDict is an array of words specific to the CPF context
var customDict = []

async function fetchLineNumber(doc, pathArray) {
  // Uses Fetch API to call our function from Flask server to get line number based on ruamel.yaml number line mapping
  // To simplify line number mapping. If there's a simpler way to do this on JS, this can be deprecated
  // WARNING: Fetch API in experimental-mode 
  return fetch('http://127.0.0.1/getLineNumber', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      docString: doc,
      pathArray: pathArray
    })
  })
    .then(response => response.json())
}

function getSubtiers(path) {
  var subtiers = path.split("/")
  var pathVersionAt = -1
  if (subtiers.length == 5) {
    pathVersionAt = 3
  }
  else if (subtiers.length == 6) {
    pathVersionAt = 4
  }
  const leftSlice = subtiers.slice(1, pathVersionAt)
  const rightSlice = subtiers.slice(pathVersionAt + 1)
  subtiers = [...leftSlice, ...rightSlice]

  return subtiers
}


// WordsNinja or Natural do not allow adding custom words during runtime or it is too expensive
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
ajv.addKeyword({
    keyword: "path-length",
    validate: function checkPathLength(schema, data, parentSchema, dataPath) {
      // Checks if the path length is 5 or 6
      if (schema == false) {
        return true
      }
      const path = dataPath["parentDataProperty"]
      const subtiers = path.split("/")
      if (subtiers.length == 5 || subtiers.length == 6) {
        return true
      }
      checkPathLength.errors = [
        {
          keyword: "path-length",
          message: "Invalid path length. Only 4 or 5 subtiers allowed",
          params: {
            pathLength: false
          }
        }
      ]
      return false
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
    var pathVersion = null
    const subtiers = path.split("/")
    if (subtiers.length == 5) {
      pathVersion = subtiers[3]
    }
    else if (subtiers.length == 6) {
      pathVersion = subtiers[4]
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
    var pathVersion = null
    const subtiers = path.split("/")
    if (subtiers.length == 5) {
      pathVersion = subtiers[3]
    }
    else if (subtiers.length == 6) {
      pathVersion = subtiers[4]
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
          message: "Version in path does not match with version in [Info]",
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
    // Checks if the subtier is in camel casing format
    // TODO: Compound words not handled
    if (schema == false) {
      return true
    }
    const subtiersNotCamelCase = []
    const path = dataPath["parentDataProperty"]
    var subtiers = getSubtiers(path)
    for (var subtier of subtiers) {
      var words = _.words(subtier) // splits subtier into words using lodash based on camel casing
      for (var word of words) {
        if (SpellChecker.isMisspelled(word) && !wordInCustomDict(word)) {
          subtiersNotCamelCase.push(subtier)
          break
        }
      }
    }
    if (subtiersNotCamelCase.length != 0) {
      const subtiersNotCamelCase_string = subtiersNotCamelCase.join(', ')
      checkCamelCasing.errors = [
        {
          keyword: "camel-casing",
          message: `The following subtier(s) are not in camel case format: "${subtiersNotCamelCase_string}"`,
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
    // Checks the spelling of all words in subtiers (because spelling-check does not apply to concatenated strings)
    // TODO: Compounds words not handled
    // TODO: Return subtiers with words spelled wrongly
    // Will not send info on words to correct because behaviour of WordsNinja not stable; possible if it separates words better
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    var subtiers = getSubtiers(path)
    for (var subtier of subtiers) {
      var words = WordsNinja.splitSentence(subtier) // split words using Wordsninja based on word identification
      for (var word of words) {
        if (SpellChecker.isMisspelled(word) && !wordInCustomDict(word)) {
          checkPathSpelling.errors = [
            {
              keyword: "path-spelling",
              message: "Word(s) in subtier(s) spelled incorrectly",
              params: {
                pathSpelling: false
              }
            }
          ]
          return false
        }
      }
    }
    return true
  }
})
ajv.addKeyword({
  keyword: "subtier-verb",
  validate: function checkSubtierVerb(schema, data, parentSchema, dataPath) {
    // Subtier verb only applies to subtiers after the version subtier
    // Checks if the first word of the subtier is a verb
    if (schema == false) {
      return true
    }
    const path = dataPath["parentDataProperty"]
    var subtiers = path.split("/")
    var pathVersionAt = -1
    if (subtiers.length == 5) {
      pathVersionAt = 3
    }
    else if (subtiers.length == 6) {
      pathVersionAt = 4
    }
    subtiers = subtiers.slice(pathVersionAt + 1) // only right slice; always only 1 subtier but we expand for extensibility

    var notVerbAndSubtiers = [] 
    for (var subtier of subtiers) {
      var words = _.words(subtier)
      var verb = words[0] // no need to catch index errors, if subtier is null, it words[0] will return null
      var taggedVerb = tagger.tag([verb]) // uses natural to do POS tagging
      var tag = taggedVerb.taggedWords[0].tag
      if (tag != "VB") {
       notVerbAndSubtiers.push([verb, subtier])
      }
    }
    if (notVerbAndSubtiers.length != 0) {
      const notVerbAndSubtiers_formatted = notVerbAndSubtiers.map(function (tuple) {
        return tuple[0] + " in " + tuple[1]
      })
      const notVerbAndSubtiers_string = notVerbAndSubtiers_formatted.join(", ") 
      checkSubtierVerb.errors = [
        {
          keyword: "subtier-verb",
          message: `The following word(s) are not verbs: ${notVerbAndSubtiers_string}`,
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
// TODO: Auto-suggestions for misspelled words
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
      const wordsSpelledWrong_string = Array.from(wordsSpelledWrong).join(', ')
      var errorMessage = `The following word(s) are spelled wrongly: ${wordsSpelledWrong_string}. Please consider adding the words into the custom dictionary or correcting them.`
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

  // const data_string = fs.readFileSync('template1.yaml', 'utf-8')
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
          // TODO: Handle error instead of just throwing
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

const hostname = 'localhost'; 
const port = 80; // we put the same port as the flask server to expose minimum number of ports, but make sure no routes are the same

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