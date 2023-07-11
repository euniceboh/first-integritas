//=======================================================================================================
//                                             Dependencies
//=======================================================================================================

const fs = require('fs');
const path = require('path')

const _ = require("lodash");

const dictionaryPath = path.join(__dirname, "..", "typojs_dictionaries")
const Typo = require("typo-js");
const dictionaryUS = new Typo("en_US")
const dictionaryUK = new Typo("en_GB-ise", false, false, {
  dictionaryPath: dictionaryPath
});

const WordsNinjaPack = require('wordsninja');
const WordsNinja = new WordsNinjaPack();

//======================================================================================================
//                                             Utils
//======================================================================================================

const customDict = ["paynow", "medi", "medisave"]

let typoJSAllDict = new Set()
const typoJSUSDictPath = path.join(__dirname, "..", "node_modules", "typo-js", "dictionaries", "en_US", "en_US.dic")
const typoJSUSDict = fs.readFileSync(typoJSUSDictPath, "utf8")
const typoJSUSDictArray = typoJSUSDict.split("\n")
typoJSUSDictArray.forEach((line) => {
    let word = line.match(/^\w+/)?.[0]
    if (word) {
        typoJSAllDict.add(word)
    }
})

const typoJSUKDictPath = path.join(__dirname, "..", "typojs_dictionaries", "en_GB-ise", "en_GB-ise.dic")
const typoJSUKDict = fs.readFileSync(typoJSUKDictPath, "utf8")
const typoJSUKDictArray = typoJSUKDict.split("\n")
typoJSUKDictArray.forEach((line) => {
    let word = line.match(/^\w+/)?.[0]
    if (word) {
      typoJSAllDict.add(word)
    }
})

customDict.forEach((word) => {
    typoJSAllDict.add(word)
})

addWordsWordsNinja([...typoJSAllDict])

function addWordsWordsNinja(wordsArray) {
  try {
    const wordsNinjaDictPath = path.join(__dirname, "..", "node_modules", "wordsninja", "words-en.txt")
    const wordsNinjaDict = fs.readFileSync(wordsNinjaDictPath, "utf8")
    const wordsNinjaDictSet = new Set(wordsNinjaDict.split("\n"))
    const wordsToAdd = wordsArray.filter((word) => !wordsNinjaDictSet.has(word))
    if (wordsToAdd.length) {
      const wordsToAddString = "\n" + wordsToAdd.join("\n")
      fs.appendFileSync(wordsNinjaDictPath, wordsToAddString, "utf8")
    }
  } catch (error) {
    console.log(error)
    throw error
  }
}

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

function checkPathCharacters(path) {
    const regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>? ]/
    return !(regex.test(path))
}

function checkPathLength(path) {
    const pathSegments = path.split("/")
    return (pathSegments.length == 4 || pathSegments.length == 5 || pathSegments.length == 6);
}

function checkAPIProduct(path) {
    const pathSegments = path.split("/")
    const apiProduct = pathSegments[1]
    const allowedAPIProducts = new Set([ 
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
                              ])
    return allowedAPIProducts.has(apiProduct);
}

function checkPathVersion(path) {
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
    return !(pathVersion == "" || pathVersion == null || !regex.test(pathVersion));
}

function checkMatchingVersion(path) {
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
  
    let infoVersionNum = 1 // hardcoded due to lack of full YAML doc examples in tests

    return (pathVersionNum == infoVersionNum)
}

function checkCamelCasing(path) {
    const pathSegmentsNotCamelCase = []
    let pathSegments = getPathSegments(path)
    for (let segment of pathSegments) {
      let words = _.words(segment)
      for (let word of words) {
        if (!wordInCustomDict(word) && !dictionaryUS.check(word) && !dictionaryUK.check(word)) {
          if (!isNaN(word)) {
            continue
          }
          pathSegmentsNotCamelCase.push(segment)
          break
        }
      }
    }
    if (pathSegmentsNotCamelCase.length != 0) {
      const pathSegmentsNotCamelCase_string = pathSegmentsNotCamelCase.join(', ')
      console.log(pathSegmentsNotCamelCase_string)
      return false
    }
    return true
}

async function checkPathSpelling(path) {
    await WordsNinja.loadDictionary()

    let pathSegments = getPathSegments(path)
    const segmentsSpelledWrongly = []
    for (let segment of pathSegments) {
      let words = WordsNinja.splitSentence(segment)
      for (let word of words) {
        if (!wordInCustomDict(word) && !dictionaryUS.check(word) && !dictionaryUK.check(word)) {
          if (!isNaN(word)) {
            continue
          }
          segmentsSpelledWrongly.push(segment)
          break
        }
      }
    }
    if (segmentsSpelledWrongly.length != 0) {
      const segmentsSpelledWrongly_string = segmentsSpelledWrongly.join(", ")
      console.log(segmentsSpelledWrongly_string)
      return false
    }
    return true
}

function checkVerb(path) {
    let pathSegments = path.split("/")
    const pathVerb = pathSegments[pathSegments.length - 1]
    if (pathVerb == '') {
      return false
    }

    let words = _.words(pathVerb)
    let verb = words[0]

    const allowedVerbs = new Set(["create", "get", "update", "delete", "compute", "transact", "check", "transfer"])

    return allowedVerbs.has(verb)
}

//================================================================

const fileContent = fs.readFileSync('./unit_test/uris.txt', 'utf8');
let paths = fileContent.split('\n')

module.exports = {
  paths,
  checkPathCharacters,
  checkPathLength,
  checkAPIProduct,
  checkPathVersion,
  checkMatchingVersion,
  checkCamelCasing,
  checkPathSpelling,
  checkVerb
}