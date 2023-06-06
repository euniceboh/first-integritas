import Ajv from "ajv"
import yaml from "js-yaml"
import fs from "fs"

const ajv = new Ajv({
  schemaId: "auto",
  allErrors: true,
  jsonPointers: true,
}) 

// const schema = yaml.load(fs.readFileSync('oas3.0_schema.yaml', 'utf-8'))
// console.log(schema)

const schema = {
  $schema: 'http://json-schema.org/draft-04/schema#',
  type: 'object',
  properties: {
    openapi: { type: 'string' },
    info: { type: 'string' },
    paths: { type: 'integer' }
  },
  required: ['openapi', 'info', 'paths']
}

const validate = ajv.compile(schema)

const data = {
  openapi: "test",
  info: "test",
  paths: 0
}

const valid = validate(data)
if (!valid) console.log(validate.errors)