const Ajv = require("ajv");
const AjvErrors = require("ajv-errors");
const AjvKeywords = require("ajv-keywords");
const addFormats = require("ajv-formats")
const yaml = require("js-yaml");
const fs = require("fs");

const schema = yaml.load(fs.readFileSync('oas3.0_schema.yaml', 'utf-8'))
const data = yaml.load(fs.readFileSync('template1.yaml', 'utf-8'))

const ajv = new Ajv({
  schemaId: "id",
  allErrors: true,
})
addFormats(ajv, ["uri-reference", "email", "regex", "uri"])
AjvErrors(ajv) // for the errorMessage keyword

// TODO: Spelling Checking Feature
// Consider using a keyword on each value for spelling checking
const spellingKeyword = {
  keyword: 'spelling',
  validate: (schema, data) => {
    if (typeof data === 'string') {
      const isSpelledCorrectly = spellchecker.isMisspelled(data);
      return !isSpelledCorrectly;
    }
    return true;
  },
  errors: true // Enable error messages for the keyword
};

// TODO: Custom Validation Rules
// Consider using a keyword on keys

const validate = ajv.compile(schema)

function getLineNumberFromPath(dataJson, pathArray) {
  if (pathArray.length == 0) {
    return 0
  }
  // TODO: Finish getting line number from path array. Can call our python function if
  // its too hard to get from JS
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
    var lineNumber = getLineNumberFromPath(data, pathArray)
    console.log(lineNumber)
    console.log(pathArray)
    console.log(validate.errors[i])
  }
}
