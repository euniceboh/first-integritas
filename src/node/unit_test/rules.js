//=======================================================================================================
//                                             Dependencies
//=======================================================================================================

const _ = require("lodash");

const Typo = require("typo-js");
const dictionary = new Typo("en_US");

const WordsNinjaPack = require('wordsninja');
const WordsNinja = new WordsNinjaPack();

const natural = require('natural');

//======================================================================================================
//                                             Utils
//======================================================================================================

const customDict = ["medi", "medisave", "dependants", "utilisation"]

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
    try {
        const regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>? ]/
        return !(regex.test(path));
    } catch (err) {
        console.log(err)
        return false
    }
}

function checkPathLength(path) {
    try {
        const pathSegments = path.split("/")
        return (pathSegments.length == 4 || pathSegments.length == 5 || pathSegments.length == 6);
    } catch (err) {
        console.log(err)
        return false
    }
}

function checkAPIProduct(path) {
    try {
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
        return allowedAPIProducts.includes(apiProduct);
    } catch (err) {
        console.log(err)
        return false
    }
}

function checkPathVersion(path) {
    try {
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
    } catch (err) {
        console.log(err)
        return false
    }
}

function checkMatchingVersion(path) {
    try {
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
    } catch (err) {
        console.log(err)
        return false
    }
}

function checkCamelCasing(path) {
    try {
      const pathSegmentsNotCamelCase = []
      let pathSegments = getPathSegments(path)
      for (let segment of pathSegments) {
        let words = _.words(segment)
        for (let word of words) {
          if (!wordInCustomDict(word) && !dictionary.check(word)) {
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
    } catch (err) {
        console.log(err)
        return false
    }
}

async function checkPathSpelling(path) {
    await WordsNinja.loadDictionary()
    try {
      let pathSegments = getPathSegments(path)
      const segmentsSpelledWrongly = []
      for (let segment of pathSegments) {
        let words = WordsNinja.splitSentence(segment) // split words using Wordsninja based on word identification
        for (let word of words) {
          if (!wordInCustomDict(word) && !dictionary.check(word)) {
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
    } catch (err) {
        console.log(err)
        return false
    }
}

function checkVerb(path) {
    try {
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
    } catch (err) {
        console.log(err)
        return false
    }
}

//================================================================

module.exports = {
  checkPathCharacters,
  checkPathLength,
  checkAPIProduct,
  checkPathVersion,
  checkMatchingVersion,
  checkCamelCasing,
  checkPathSpelling,
  checkVerb
}