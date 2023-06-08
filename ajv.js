const Ajv = require("ajv");
const AjvErrors = require("ajv-errors");
const AjvKeywords = require("ajv-keywords");
const addFormats = require("ajv-formats")
const yaml = require("js-yaml");
const fs = require("fs");
const WordsNinjaPack = require('wordsninja');
const WordsNinja = new WordsNinjaPack();

const schema_string = fs.readFileSync('oas3.0_schema.yaml', 'utf-8')
const schema = yaml.load(schema_string)
const data_string = fs.readFileSync('template1.yaml', 'utf-8')
const data = yaml.load(data_string)
  

const ajv = new Ajv({
  schemaId: "id",
  allErrors: true,
})
addFormats(ajv, ["uri-reference", "email", "regex", "uri"])
AjvErrors(ajv) // add all ajv-errors keywords, significantly, errorMessage
require("ajv-keywords")(ajv) // add all ajv-keywords keywords

// TODO: Spelling Checking Feature
// Consider using a keyword on each value for spelling checking
// const spellingKeyword = {
//   keyword: 'spelling',
//   validate: (schema, data) => {
//     if (typeof data === 'string') {
//       const isSpelledCorrectly = spellchecker.isMisspelled(data);
//       return !isSpelledCorrectly;
//     }
//     return true;
//   },
//   errors: true // Enable error messages for the keyword
// };

// TODO: Custom Validation Rules
// Consider using a keyword on keys
// validate: schema (value of the check key), data (value of the checking key), parentSchema, dataPath
function checkPathCharacters(schema, data, parentSchema, dataPath) {
  const path = dataPath["parentDataProperty"]
  const regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>? ]/
  if (regex.test(path)) {
    return schema == false
  }
  return schema == true
}

function checkPathLength(schema, data, parentSchema, dataPath) {
  const path = dataPath["parentDataProperty"]
  const subtiers = path.split("/")
  if (subtiers.length == 5 || subtiers.length == 6) {
    return schema == true
  }
  return schema == false
}

function checkPathVersion(schema, data, parentSchema, dataPath) {
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
    return schema == false
  }
  return schema == true
}

function checkMatchingVersion(schema, data, parentSchema, dataPath) {
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
    return schema == false
  }

  if (pathVersionNum != infoVersionNum) {
    return schema == false
  }
  return schema == true
}

var dict = ["medi"]
// split --> check spelling --> check camelCase --> check verb
function checkSubtierVerb(schema, data, parentSchema, dataPath, dict) {
  const path = dataPath["parentDataProperty"]
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
  
  // for (let i = 0; i < subtiers.length; i++) {
    
    
  // }
  return true
}

// lodash
function checkCamelCasing(schema, data, parentSchema, dataPath) {

}

// typo.js
function checkPathSpelling(schema, data, parentSchema, dataPath) {

}

// maybe possible to implement without custom keywords
function checkProperties(schema, data, parentSchema, dataPath) {

}

ajv.addKeyword({
    keyword: "path-characters", // keywords should be delimited by "-" to avoid future name collisions
    validate: checkPathCharacters,
    errors: false
})
ajv.addKeyword({
    keyword: "path-length",
    validate: checkPathLength,
    errors: false
})
ajv.addKeyword({
  keyword: "path-version",
  validate: checkPathVersion,
  error: {
    message: "Invalid or missing path version"
  }
})
ajv.addKeyword({
  keyword: "match-version",
  validate: checkMatchingVersion,
  errors: false
})
ajv.addKeyword({
  keyword: "subtier-verb",
  validate: checkSubtierVerb,
  errors: false
})

const validate = ajv.compile(schema)


function fetchLineNumber() {
  return fetch('http://127.0.0.1/getLineNumber', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      docString: data_string,
      pathArray: pathArray
    })
  })
    .then(response => response.json())
}

if (!validate(data)) {
  for (let i = 0; i < validate.errors.length; i++) {
    if (["if", "then", "else"].includes(validate.errors[i]["keyword"])) {
      continue;
    }
    var path = validate.errors[i]["instancePath"]
    var pathArray = path.split("/").slice(1,)
    // change back "/" that are converted from ajv
    for (let j = 0; j < pathArray.length; j++) {
      if (pathArray[j]) {
        pathArray[j] = pathArray[j].replace(/~1/g, "/")
      }
    }
    var line = -1;

    fetchLineNumber()
      .then(data => {
        line = data["lineNumber"]
      })
      .then(final => {
        console.log(line)
        console.log(validate.errors[i])
      })

    
  }
}
