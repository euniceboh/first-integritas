// JEST White-Box Unit Testing

const rules = require('./unit_test');

const paths = rules.paths

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

let path_fail_checkPathCharacters = "/medicalInsurance/medi-ShieldLife/v1/getMemberDependants"
test(`Fail checkPathCharacters --- ${path_fail_checkPathCharacters}`, () => {
    expect(rules.checkPathCharacters(path_fail_checkPathCharacters)).toBe(false)
})

let path_fail_checkPathLength = "/medicalInsurance/mediShieldLife/subtier2/subtier3/v1/getMemberDependants"
test(`Fail checkPathLength --- ${path_fail_checkPathLength}`, () => {
    expect(rules.checkPathLength(path_fail_checkPathLength)).toBe(false)
})

let path_fail_checkAPIProduct = "/productNotExist/mediShieldLife/v1/getMemberDependants"
test(`Fail checkAPIProduct --- ${path_fail_checkAPIProduct}`, () => {
    expect(rules.checkAPIProduct(path_fail_checkAPIProduct)).toBe(false)
})

let path_fail_checkPathVersion = "/medicalInsurance/mediShieldLife/b2/getMemberDependants"
test(`Fail checkPathVersion --- ${path_fail_checkPathVersion}`, () => {
    expect(rules.checkPathVersion(path_fail_checkPathVersion)).toBe(false)
})

let path_fail_checkMatchingVersion = "/medicalInsurance/mediShieldLife/v2/getMemberDependants"
test(`Fail checkMatchingVersion --- ${path_fail_checkMatchingVersion}`, () => {
    expect(rules.checkMatchingVersion(path_fail_checkMatchingVersion)).toBe(false)
})

let path_fail_checkCamelCasing = "/medicalInsurance/mediShieldlife/v1/getMemberdepenants"
test(`Fail checkCamelCasing --- ${path_fail_checkCamelCasing}`, () => {
    expect(rules.checkCamelCasing(path_fail_checkCamelCasing)).toBe(false)
})

let path_fail_checkPathSpelling = "/medicalInsurance/mediShieldLfe/v1/getMemberDepeants"
test(`Fail checkPathSpelling --- ${path_fail_checkPathSpelling}`, async () => {
    expect(await rules.checkPathSpelling(path_fail_checkPathSpelling)).toBe(false)
})

let path_fail_checkPathVerb = "/medicalInsurance/mediShieldLife/v1/parisMemberDependants"
test(`Fail checkPathVerb --- ${path_fail_checkPathVerb}`, () => {
    expect(rules.checkVerb(path_fail_checkPathVerb)).toBe(false)
})