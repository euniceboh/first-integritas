//============================================================================================
//                                    Dependencies
//============================================================================================
const Ajv = require("ajv");
const AjvErrors = require("ajv-errors");
const AjvKeywords = require("ajv-keywords");
const addFormats = require("ajv-formats");

const yaml = require("js-yaml");

const fs = require("fs");

const _ = require("lodash");

const Typo = require("typo-js");
const dictionary = new Typo("en_US");

const WordsNinjaPack = require('wordsninja');
const WordsNinja = new WordsNinjaPack();

const natural = require('natural');
const tokenizer = new natural.WordTokenizer();

const express = require("express")
const bodyParser = require("body-parser")
const cors = require("cors")

//============================================================================================
//                                    Routes
//============================================================================================

const app = express()
app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

// toggle port 3000 when releasing locally and 80 when releasing to azure
const port = 80

app.get("/", (req, res) => {
  res.send("Welcome to the backend server of CPF OAS Validator Tool!")
})

app.post("/validate", async (req, res) => {
  try {
    // let data = JSON.parse(req.body)
    let docString = req.body.doc
    let dictionaryArray = req.body.dictionary
    let payload = await validateYAML(docString, dictionaryArray)
    if (payload == null) { // error with validation logic
      res.status(500).json({msg: "Validation logic error"})
    }
    else if (payload.length == 0) { // valid yaml doc
      res.status(204).json({msg: "Successful!"})
    }
    else { // invalid yaml doc
      res.status(200).json(payload)
    }
  } catch (error) { // unexpected error
    res.status(500).json({msg: "Unexpected error"})
  }
})

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});

//============================================================================================
//                                    Utils
//============================================================================================

let customDict = []

/**
 * Invokes Ajv schema validation with custom validation rules
 * Calls function to get line number of each error from Flask server
 * Returns a list of formatted error objects
 * 
 * @function
 * @param {string} docString 
 * @param {Array} dictionaryArray 
 */
async function validateYAML(docString, dictionaryArray) { 
  await WordsNinja.loadDictionary(); // forced async load by WordsNinja library
  customDict = dictionaryArray;

  let validate = false
  try {
    const schemaString = fs.readFileSync('oas3.0_schema.yaml', 'utf-8')
    const schema = yaml.load(schemaString)
    validate = ajv.compile(schema)
  }
  catch {
    return null
  }

  let doc = null
  try {
    doc = yaml.load(docString)
  } catch {
    return null
  }
  
  let payload = []
  if (!validate(doc)) {
    for (let error of validate.errors) {
      if (["if", "then", "else"].includes(error["keyword"])) { // if/then/else errors are ignored and replaced by more useful error messages
        continue;
      }
      let path = error["instancePath"]
      let pathArray = path.split("/").slice(1,)
      
      for (let j = 0; j < pathArray.length; j++) { // change back "/" that are converted from Ajv
        if (pathArray[j]) {
          pathArray[j] = pathArray[j].replace(/~1/g, "/")
        }
      }

      let line = -1;
      await fetchLineNumber(docString, pathArray)
        .then((data) => {
          line = data["lineNumber"]
        })
        .catch(() => {
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

/**
 * Uses Fetch API to call our function from Flask server to get line number based on ruamel.yaml number line mapping
 * Returns line number of error
 * If there's a simpler way to do this on JS, this can be deprecated 
 * 
 * @function
 * @param {string} docString
 * @param {Array} pathArray 
 */
async function fetchLineNumber(docString, pathArray) {
  try {
    // const response = await fetch("http://flask/getLineNumber", {
    const response = await fetch("https://cpfdevportal.azurewebsites.net/getLineNumber", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        doc: docString,
        path: pathArray
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

/**
 * Slices path depending on number of segments, excluding the version number segment
 * Returns the path segments as an array of strings
 * 
 * @function
 * @param {string} path 
 */
function getPathSegments(path) {
  let pathSegments = path.split("/")
  let pathVersionAt = -1
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
/**
 * Checks if the word passed as parameter is in the custom dictionary
 * Returns true if it is, false if not
 * 
 * @function
 * @param {string} word 
 */
function wordInCustomDict(word) {
  for (let customWord of customDict) {
    if (word.toLowerCase() == customWord.toLowerCase()) {
      return true
    }
  }
  return false
}

//======================================================================================================
//                     Ajv Custom Validation Rules (CPFB API Standards v1.1.2)
//======================================================================================================
const ajv = new Ajv({
  schemaId: "id",
  allErrors: true,
})
addFormats(ajv, ["uri-reference", "email", "regex", "uri"])
AjvErrors(ajv) // add all ajv-errors keywords, significantly, errorMessage
require("ajv-keywords")(ajv) // add all ajv-keywords keywords

/**
 * Checks for special characters in path, except for "/"
 */
ajv.addKeyword({
    keyword: "path-characters", 
    validate: function checkPathCharacters(schema, data, parentSchema, dataPath) {
      if (!schema) {
        return true
      }
      try {
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
      } catch {
        checkPathCharacters.errors = [
          {
            keyword: "path-characters",
            message: "Unexpected error in validation function",
            params: {
              pathCharacters: false
            }
          }
        ]
        return false
      }
    }
})
/**
 * Checks if the path length is valid (4, 5, or 6)
 * Internal API Route format: /<API Product>/<Subtier 1>/<Subtier 2>/<VersionNum>/<Verb>
 * Subtiers are optional
 */
ajv.addKeyword({ 
    keyword: "path-length",
    validate: function checkPathLength(schema, data, parentSchema, dataPath) {
      if (!schema) {
        return true
      }
      try {
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
      } catch {
        checkPathLength.errors = [
          {
            keyword: "path-length",
            message: "Unexpected error in validation function",
            params: {
              pathLength: false
            }
          }
        ]
        return false
      }
    }
})
/**
 * Checks for valid API Product
 * WARNING: Hardcoded API Product array
 */
ajv.addKeyword({
  keyword: "api-product",
  validate: function checkAPIProduct(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const path = dataPath["parentDataProperty"]
      const pathSegments = path.split("/")
      const apiProduct = pathSegments[1]
      const allowedAPIProducts = [ 
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
            message: "Invalid API Product",
            params: {
              apiProduct: false
            }
          }
        ]
        return false
      }
      return true
    } catch {
      checkAPIProduct.errors = [
        {
          keyword: "api-product",
          message: "Unexpected error in validation function",
          params: {
            apiProduct: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Checks if path version segment exists in path
 */
ajv.addKeyword({
  keyword: "path-version",
  validate: function checkPathVersion(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const path = dataPath["parentDataProperty"]
      const pathSegments = path.split("/")
      let pathVersion = null
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
    } catch {
      checkPathVersion.errors = [
        {
          keyword: "path-version",
          message: "Unexpected error in validation function",
          params: {
            pathVersion: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Checks if the version in path matches the version in <info>
 */
ajv.addKeyword({
  keyword: "match-version",
  validate: function checkMatchingVersion(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const path = dataPath["parentDataProperty"]
      const pathSegments = path.split("/")
      let pathVersion = null
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
    
      let infoVersionNum = -1
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
    } catch {
      checkMatchingVersion.errors = [
        {
          keyword: "match-version",
          message: "Unexpected error in validation function",
          params: {
            matchVersion: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Checks if the path segment is in camel casing format
 * WARNING: Compound words are not handled
 * WARNING: Words in the UK dictionary are not handled
 */
ajv.addKeyword({
  keyword: "camel-casing",
  validate: function checkCamelCasing(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const pathSegmentsNotCamelCase = []
      const path = dataPath["parentDataProperty"]
      let pathSegments = getPathSegments(path)
      for (let segment of pathSegments) {
        let words = _.words(segment) // splits subtier into words using lodash based on camel casing
        for (let word of words) {
          if (!isNaN(word)) {
            continue
          }
          if (!wordInCustomDict(word) && !dictionary.check(word)) {
            pathSegmentsNotCamelCase.push(segment)
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
    } catch {
      checkCamelCasing.errors = [
        {
          keyword: "camel-casing",
          message: "Unexpected error in validation function",
          params: {
            camelCasing: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Checks the spelling of all words in segments (because spelling-check does not apply to concatenated strings)
 * Not advised to send info on words to correct because behaviour of WordsNinja not stable; possible if it separates words better
 * WARNING: Compound words are not handled
 * WARNING: Words in the UK dictionary are not handled
 */
ajv.addKeyword({
  keyword: "path-spelling",
  validate: function checkPathSpelling(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const segmentsSpelledWrongly = []
      const path = dataPath["parentDataProperty"]
      let pathSegments = getPathSegments(path)
      for (let segment of pathSegments) {
        let words = WordsNinja.splitSentence(segment) // split words using Wordsninja based on word identification
        for (let word of words) {
          if (!isNaN(word)) {
            continue
          }
          if (!wordInCustomDict(word) && !dictionary.check(word)) {
            segmentsSpelledWrongly.push(segment)
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
    } catch {
      checkPathSpelling.errors = [
        {
          keyword: "path-spelling",
          message: "Unexpected error in validation function",
          params: {
            pathSpelling: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Checks if <Verb> in path is an allowed verb
 */
ajv.addKeyword({ 
  keyword: "path-verb",
  validate: function checkVerb(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const path = dataPath["parentDataProperty"]
      let pathSegments = path.split("/")
      const pathVerb = pathSegments[pathSegments.length - 1]
      let words = _.words(pathVerb)
      let verb = words[0]
  
      const allowedVerbs = ["create", "get", "update", "delete", "compute", "transact", "check", "transfer"]
  
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
    } catch {
      checkVerb.errors = [
        {
          keyword: "path-verb",
          message: "Unexpected error in validation function",
          params: {
            subtierVerb: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Checks if elements in <required> are present in <properties>
 */
ajv.addKeyword({
  keyword: "required-properties",
  validate: function checkProperties(schema, data, parentSchema, dataPath) { 
    if (!schema) {
      return true
    }
    try {
      const propertiesNotPresent = []                                                                                                                                                                                                                                                                                          
      const parentData = dataPath["parentData"]
      const propertiesList = Object.keys(parentData["properties"])
      const requiredList = parentData["required"]
      for (let requiredProperty of requiredList) {
        if (!propertiesList.includes(requiredProperty)) {
          propertiesNotPresent.push(requiredProperty)
        }
      }
      if (propertiesNotPresent.length > 0) {
        const propertiesNotPresent_string = propertiesNotPresent.join(", ")
        checkProperties.errors = [
          {
            keyword: "required-properties",
            message: `The following properties are not present: ${propertiesNotPresent_string}`,
            params: {
              requiredProperties: false
            }
          }
        ]
        return false
      }
      return true
    } catch {
      checkProperties.errors = [
        {
          keyword: "required-properties",
          message: "Unexpected error in validation function",
          params: {
            requiredProperties: false
          }
        }
      ]
      return false
    }
  }
})
/**
 * Spelling checks sentences
 * Mainly used on description and titles and excludes extensions (e.g., x-author)
 * WARNING: Words in the UK dictionary are not handled
 */
ajv.addKeyword({
  keyword: "spelling-check",
  validate: function checkSpelling(schema, data, parentSchema, dataPath) {
    if (!schema) {
      return true
    }
    try {
      const words = tokenizer.tokenize(data)
      let wordsSpelledWrong = new Set()
      for (let word of words) {
        if (!isNaN(word)) {
          continue
        }
        if (!wordInCustomDict(word) && !dictionary.check(word)) {
          wordsSpelledWrong.add(word)
        }
      }
      if (wordsSpelledWrong.size != 0) {
        let formattedWordsSpelledWrong = ''
        wordsSpelledWrong.forEach(word => {formattedWordsSpelledWrong += `- ${word} ==> ${dictionary.suggest(word).join(", ")}<br>`})
        let errorMessage = 'The following word(s) are spelled incorrectly in this field:' + '<br>' + formattedWordsSpelledWrong
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
    } catch {
      checkSpelling.errors = [
        {
          keyword: 'spelling-check',
          message: "Unexpected error in validation function",
          params: {
            checkSpelling: false
          }
        }
      ]
    }
  }
})