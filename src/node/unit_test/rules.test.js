const rules = require('./rules');
const fs = require('fs');

const fileContent = fs.readFileSync('./unit_test/uris.txt', 'utf8');
let paths = fileContent.split('\r\n');

for (let path of paths) {
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









