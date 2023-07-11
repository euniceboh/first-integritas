// JEST White-Box Unit Testing
// Functions are invoked in sequence in app so there is no need to test initial edge cases in later tests

const rules = require('./unit_test');

const paths = rules.paths

const path_allPass = "/discretionaryWithdrawals/55Withdrawals/v1/updateMemberCreditStatusForPayNow"

//==============================checkPathCharacters============================================
test(`Pass checkPathCharacters --- ${path_allPass}`, () => {
    expect(rules.checkPathCharacters(path_allPass)).toBe(true)
})

const path_fail_checkPathCharacters = "/medicalInsurance/medi-ShieldLife/v1/getMemberDependants"
test(`Fail checkPathCharacters --- ${path_fail_checkPathCharacters}`, () => {
    expect(rules.checkPathCharacters(path_fail_checkPathCharacters)).toBe(false)
})

//==============================checkPathLength================================================
test(`Pass checkPathLength --- ${path_allPass}`, () => {
    expect(rules.checkPathLength(path_allPass)).toBe(true)
})

const path_fail_checkPathLength_lowerBound = "/medicalInsurance"
test(`Fail checkPathLength lowerBound --- ${path_fail_checkPathLength_lowerBound}`, () => {
    expect(rules.checkPathLength(path_fail_checkPathLength_lowerBound)).toBe(false)
})

const path_fail_checkPathLength_upperBound = "/medicalInsurance/mediShieldLife/subtier2/subtier3/v1/getMemberDependants"
test(`Fail checkPathLength upperBound --- ${path_fail_checkPathLength_upperBound}`, () => {
    expect(rules.checkPathLength(path_fail_checkPathLength_upperBound)).toBe(false)
})

//==============================checkAPIProduct================================================
test(`Pass checkAPIProduct --- ${path_allPass}`, () => {
    expect(rules.checkAPIProduct(path_allPass)).toBe(true)
})

let path_fail_checkAPIProduct = "/productNotExist/mediShieldLife/v1/getMemberDependants"
test(`Fail checkAPIProduct --- ${path_fail_checkAPIProduct}`, () => {
    expect(rules.checkAPIProduct(path_fail_checkAPIProduct)).toBe(false)
})

//==============================checkPathVersion================================================
test(`Pass checkPathVersion --- ${path_allPass}`, () => {
    expect(rules.checkPathVersion(path_allPass)).toBe(true)
})

let path_fail_checkPathVersion_empty = "/medicalInsurance/mediShieldLife//getMemberDependants"
test(`Fail checkPathVersion empty --- ${path_fail_checkPathVersion_empty}`, () => {
    expect(rules.checkPathVersion(path_fail_checkPathVersion_empty)).toBe(false)
})

let path_fail_checkPathVersion_wrongLetter = "/medicalInsurance/mediShieldLife/b2/getMemberDependants"
test(`Fail checkPathVersion wrongLetter --- ${path_fail_checkPathVersion_wrongLetter}`, () => {
    expect(rules.checkPathVersion(path_fail_checkPathVersion_wrongLetter)).toBe(false)
})

let path_fail_checkPathVersion_wrongNumber = "/medicalInsurance/mediShieldLife/vb/getMemberDependants"
test(`Fail checkPathVersion wrongNumber --- ${path_fail_checkPathVersion_wrongNumber}`, () => {
    expect(rules.checkPathVersion(path_fail_checkPathVersion_wrongNumber)).toBe(false)
})

//==============================checkMatchingVersion================================================
// See unit_test.js; info version assumed to be v1
test(`Pass checkMatchingVersion --- ${path_allPass}`, () => {
    expect(rules.checkMatchingVersion(path_allPass)).toBe(true)
})

let path_fail_checkMatchingVersion = "/medicalInsurance/mediShieldLife/v2/getMemberDependants"
test(`Fail checkMatchingVersion --- ${path_fail_checkMatchingVersion}`, () => {
    expect(rules.checkMatchingVersion(path_fail_checkMatchingVersion)).toBe(false)
})

//==============================checkCamelCasing================================================
test(`Pass checkCamelCasing --- ${path_allPass}`, () => {
    expect(rules.checkCamelCasing(path_allPass)).toBe(true)
})

let path_fail_checkCamelCasing = "/medicalInsurance/mediShieldlife/v1/getMemberdepenants"
test(`Fail checkCamelCasing --- ${path_fail_checkCamelCasing}`, () => {
    expect(rules.checkCamelCasing(path_fail_checkCamelCasing)).toBe(false)
})

//==============================checkPathSpelling================================================
test(`Pass checkPathSpelling --- ${path_allPass}`, async () => {
    expect(await rules.checkPathSpelling(path_allPass)).toBe(true)
})

let path_fail_checkPathSpelling = "/medicalInsurance/mediShieldLfe/v1/getMemberDepeants"
test(`Fail checkPathSpelling --- ${path_fail_checkPathSpelling}`, async () => {
    expect(await rules.checkPathSpelling(path_fail_checkPathSpelling)).toBe(false)
})

//==============================checkVerb================================================
test(`Pass checkVerb --- ${path_allPass}`, () => {
    expect(rules.checkVerb(path_allPass)).toBe(true)
})

let path_fail_checkPathVerb_empty = "/medicalInsurance/mediShieldLife/v1/"
test(`Fail checkVerb --- ${path_fail_checkPathVerb_empty}`, () => {
    expect(rules.checkVerb(path_fail_checkPathVerb_empty)).toBe(false)
})

let path_fail_checkPathVerb_invalidVerb = "/medicalInsurance/mediShieldLife/v1/parisMemberDependants"
test(`Fail checkVerb --- ${path_fail_checkPathVerb_invalidVerb}`, () => {
    expect(rules.checkVerb(path_fail_checkPathVerb_invalidVerb)).toBe(false)
})

// Unit test all verified URIs provided in SharePoint
for (const path of paths) {
    test(`checkPathCharacters -- ${path}`, () => {
        expect(rules.checkPathCharacters(path)).toBe(true)
    })
    test(`checkPathLength -- ${path}`, () => {
        expect(rules.checkPathLength(path)).toBe(true);
    });
    test(`checkAPIProduct -- ${path}`, () => {
        expect(rules.checkAPIProduct(path)).toBe(true);
    });
    test(`checkPathVersion -- ${path}`, () => {
        expect(rules.checkPathVersion(path)).toBe(true);
    });
    test(`checkMatchingVersion -- ${path}`, () => {
        expect(rules.checkMatchingVersion(path)).toBe(true);
    });
    test(`checkCamelCasing -- ${path}`, () => {
        expect(rules.checkCamelCasing(path)).toBe(true);
    });
    test(`checkPathSpelling -- ${path}`, async () => {
        expect(await rules.checkPathSpelling(path)).toBe(true);
    });
    test(`checkVerb -- ${path}`, () => {
        expect(rules.checkVerb(path)).toBe(true);
    });
}