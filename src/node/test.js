const _ = require("lodash");

const SpellChecker = require('spellchecker');

const WordsNinjaPack = require('wordsninja');
const WordsNinja = new WordsNinjaPack();

const natural = require('natural');
const tokenizer = new natural.WordTokenizer();

// Path Format: /<API Product>/<Subtier 1>/<Subtier 2>/<VersionNum>/<Verb>
// const path = "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow"
// const path = '/discretionaryWithdrawals/55Withdrawals/v2/checkMemberAgeEligibility'
const path = "/medicalInsurance/mediShieldLife/v1/getPatientCoverageInfo"


//============================================================================

const customDict = []

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

//============================================================================

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
    
      let infoVersionNum = 1
      // try {
      //   infoVersionNum = dataPath["rootData"]["info"]["version"][0] 
      // } catch (error) {
      //   checkMatchingVersion.errors = [
      //     {
      //       keyword: "match-version",
      //       message: "Missing version in [Info]",
      //       params: {
      //         matchVersion: false
      //       }
      //     }
      //   ]
      //   return false
      // }

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
          if (!wordInCustomDict(word) && SpellChecker.isMisspelled(word)) {
            subtiersNotCamelCase.push(segment)
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

function checkPathSpelling(path) {
    try {
      let pathSegments = getPathSegments(path)
      const segmentsSpelledWrongly = []
      for (let segment of pathSegments) {
        console.log(segment)
        let words = WordsNinja.splitSentence(segment) // split words using Wordsninja based on word identification
        console.log(words)
        for (let word of words) {
          if (!wordInCustomDict(word) && SpellChecker.isMisspelled(word)) {
            subtiersSpelledWrongly.push(segment)
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

// test('checkPathCharacters', () => {
//   expect(checkPathCharacters(path)).toBe(true);
// });
// test('checkPathLength', () => {
//   expect(checkPathLength(path)).toBe(true);
// });
// test('checkAPIProduct', () => {
//   expect(checkAPIProduct(path)).toBe(true);
// });
// test('checkPathVersion', () => {
//   expect(checkPathVersion(path)).toBe(true);
// });
// test('checkMatchingVersion', () => {
//   expect(checkMatchingVersion(path)).toBe(true);
// });
// test('checkCamelCasing', () => {
//   expect(checkCamelCasing(path)).toBe(true);
// });
// test('checkPathSpelling', () => {
//   expect(checkPathSpelling(path)).toBe(true);
// });
// test('checkVerb', () => {
//   expect(checkVerb(path)).toBe(true);
// });

async function main() {
  await WordsNinja.loadDictionary()

  console.log(checkPathCharacters(path))
  console.log(checkPathLength(path))
  console.log(checkAPIProduct(path))
  console.log(checkPathVersion(path))
  console.log(checkMatchingVersion(path))
  console.log(checkCamelCasing(path))
  console.log(checkPathSpelling(path))
  console.log(checkVerb(path))
}

main()