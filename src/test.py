import re
import yaml
from collections import defaultdict
from pykwalify.core import Core
from pykwalify.errors import SchemaError
from cerberus import Validator
import ruamel.yaml

class Str(ruamel.yaml.scalarstring.ScalarString):
    __slots__ = ('lc')

    style = ""

    def __new__(cls, value):
        return ruamel.yaml.scalarstring.ScalarString.__new__(cls, value)

class MyPreservedScalarString(ruamel.yaml.scalarstring.PreservedScalarString):
    __slots__ = ('lc')

class MyDoubleQuotedScalarString(ruamel.yaml.scalarstring.DoubleQuotedScalarString):
    __slots__ = ('lc')

class MySingleQuotedScalarString(ruamel.yaml.scalarstring.SingleQuotedScalarString):
    __slots__ = ('lc')

class MyConstructor(ruamel.yaml.constructor.RoundTripConstructor):
    def construct_yaml_omap(self, node):
        omap = ruamel.yaml.comments.CommentedOrderedMap()
        self.construct_mapping(node, omap)
        return omap

    def construct_scalar(self, node):
        # type: (Any) -> Any
        if not isinstance(node, ruamel.yaml.nodes.ScalarNode):
            raise ruamel.yaml.constructor.ConstructorError(
                None, None,
                "expected a scalar node, but found %s" % node.id,
                node.start_mark)

        if node.style == '|' and isinstance(node.value, str):
            ret_val = MyPreservedScalarString(node.value)
        elif bool(self._preserve_quotes) and isinstance(node.value, str):
            if node.style == "'":
                ret_val = MySingleQuotedScalarString(node.value)
            elif node.style == '"':
                ret_val = MyDoubleQuotedScalarString(node.value)
            else:
                ret_val = Str(node.value)
        else:
            ret_val = Str(node.value)
        ret_val.lc = ruamel.yaml.comments.LineCol()
        ret_val.lc.line = node.start_mark.line
        ret_val.lc.col = node.start_mark.column
        return ret_val

# For Specification Extensions
def check_extension(field, value, error):
    extension_pattern = f'^x-.+'
    regex = re.compile(extension_pattern)
    if regex.match(field) is None: # field does not match the regex
        error(field, "Must start with 'x-'")

def check_path(field, value, error):
    path_pattern = f'^/.+'
    regex = re.compile(path_pattern)
    if regex.match(field) is None: # field does not match the regex
        error(field, "Must start with '/'")

# RFC 6838
def check_media_type(field, value, error):
    media_types = ["application/json",
                   "application/xml",
                   "application/x-www-form-urlencoded",
                   "multipart/form-data",
                   "text/plain; charset=utf-8",
                   "text/html",
                   "application/pdf",
                   "image/png",
                   "application/vnd.mycompany.myapp.v2+json",
                   "application/vnd.ms-excel",
                   "application/vnd.openstreetmap.data+xml",
                   "application/vnd.github-issue.text+json",
                   "application/vnd.github.v3.diff",
                   "image/vnd.djvu"]
    if field not in media_types:
        error(field, "Field not compliant with RFC 6838")

def check_url(field, value, error):
    url_pattern = f'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    regex = re.compile(url_pattern)
    if regex.match(value) is None:
        error(field, "Invalid URL")

def check_status_code(field, value, error):
    status_code_pattern = f'^(?:1\d{2}|2\d{2}|3[0-9]{2}|4[0-9]{2}|5[0-9]{2})$'
    regex = re.compile(status_code_pattern)
    if field != "default" or regex.match(value) is None:
        error(field, "Invalid status code")

def check_list_unique(field, value, error):
    duplicates = set()
    for item in value:
        if value.count(item) > 1:
            duplicates.add(item)
    if duplicates:
        error(field, "List not unique. Duplicates: " + ", ".join(duplicates))
        
# def check_or(field, value, error):
#     if value and "$ref" in value.keys():
#         if len(value.keys()) > 1:
#             error(field, "No other fields should be present with '$ref'")

doc = '''openapi: 3.0.0
info:
  title: grvrws
  description: This API is to update the crediting status of the member's 55 WDL Application for PayNow
  version: 1.0.0
  x-author: 
  x-date: '2022-12-22'

paths:
  dummy:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                Section:
                  type: object
                  description: The main request body
                  properties:
                    programId:
                      type: string
                      description: Program ID of the consumer
                      example: 'ESERVICE'
                      minLength: 1
                      maxLength: 10
                    userId:
                      type: string
                      description: User ID of the consumer
                      example: 'RSD001'
                    accountNumber:
                      type: string
                      description: Member's Account Number
                      example: 'S1234567A'
                      minLength: 9
                      maxLength: 9
                    electronicFormTransactionNumber:
                      type: string
                      description: electronicForm Transaction Number
                      example: '1500142799903518'
                      maxLength: 16
                    creditStatusTag:
                      type: string
                      description: Credit Status Tag
                      example: 'Y'
                      maxLength: 1
                    ocbcTransactionNumber:
                      type: string
                      description: OCBC Transaction Number
                      example: '20200928034440888853'
                      maxLength: 20
                    ocbcReturnCode:
                      type: string
                      description: OCBC Return Code
                      example: ''
                      maxLength: 4
                    guid:
                      type: string
                      description: The GUID of the API call
                      example: '123456789012345678901234567890123456'
                      maxLength: 36
                  required:
                    - programId
                    - accountNumber
                    - electronicFormTransactionNumber
                    - creditStatusTag
                    - ocbcTransactionNumber
                    - ocbcReturnCode
                    - guid
              required:
                - Section
      responses:
        '200':
          description: Successfully called the API to update credit status of Member's 55 WDL Application for PayNow. This can include application and data error.
          content:
            application/json:
              schema:
                type: object
                properties:
                  Section:
                    type: object
                    description: The main response body
                    properties:
                        programId:
                          type: string
                          description: Program ID of the consumer
                          example: 'ESERVICE'
                          minLength: 1
                          maxLength: 10
                        userId:
                          type: string
                          description: User ID of the consumer
                          example: 'RSD001'
                        accountNumber:
                          type: string
                          description: Member's Account Number
                          example: 'S1234567A'
                          minLength: 9
                          maxLength: 9
                        electronicFormTransactionNumber:
                          type: string
                          description: electronicForm Transaction Number
                          example: '1500142799903518'
                          maxLength: 16
                        creditStatusTag:
                          type: string
                          description: Credit Status Tag
                          example: 'Y'
                          maxLength: 1
                        ocbcTransactionNumber:
                          type: string
                          description: OCBC Transaction Number
                          example: '20200928034440888853'
                          maxLength: 20
                        ocbcReturnCode:
                          type: string
                          description: OCBC Return COde
                          example: ''
                          maxLength: 4
                        returnCode:
                          type: string
                          description: Program Return Code
                          example: '0000'
                          maxLength: 4
                        returnMessage:
                          type: string
                          description: Program Return Message
                          example: 'Successful'
                          maxLength: 50
                        guid:
                          type: string
                          description: The GUID of the API call
                          example: '123456789012345678901234567890123456'
                          maxLength: 36
                    required:
                        - programId
                        - accountNumber
                        - electronicFormTransactionNumber
                        - creditStatusTag
                        - ocbcTransactionNumber
                        - ocbcReturnCode
                        - returnCode
                        - returnMessage
                        - guid
                required:
                  - Section'''

# can add custom function checks for all of the fields
# going to do the ones corresponding to the templates given first
schema = {
    'allow_unknown': {
        'check_with': check_extension
    },
    'openapi': {
        'required': True,
        'type': 'string',
        'allowed': ['2.0', '3.0.0', '3.0.3', '3.1.0']
    },
    'info': {
        'required': True,
        'type': 'dict',
        'allow_unknown': {
            'check_with': check_extension
        },
        'schema': {
            'title': {
                'required': True,
                'type': 'string'
            },
            'version': {
                'required': True,
                'type': 'string'
            },
            'description': {
                'type': 'string'
            },
            'termsOfService': {
                'type': 'string'
            },
            'contact': {
                'type': 'dict',
                'allow_unknown': {
                  'check_with': check_extension
                },
                'schema': {
                    'name': {
                        'type': 'string'
                    },
                    'url': {
                        'type': 'string'
                    },
                    'email': {
                        'type': 'string'
                    }
                }
            },
            'license': {
                'type': 'dict',
                'allow_unknown': {
                  'check_with': check_extension
                },
                'schema': {
                    'name': {
                        'required': True,
                        'type': 'string'
                    },
                    'url': {
                        'type': 'string'
                    }
                }
            }
        }
    },
    'servers': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'allow_unknown': {
              'check_with': check_extension
            },
            'schema': {
                'url': {
                    'required': True,
                    'type': 'string'
                },
                'description': {
                    'type': 'string'
                },
                'variables': {
                    'type': 'dict',
                    'valuesrules': {
                        'type': 'dict',
                        'allow_unknown': {
                          'check_with': check_extension
                        },
                        'schema': {
                            'enum': {
                                'type': 'list',
                                'schema': {
                                    'type': 'string'
                                }
                            },
                            'default': {
                                'required': True,
                                'type': 'string'
                            },
                            'description': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    },
    'paths': {
        'required': True,
        'type': 'dict',
        'keysrules': {
            'anyof': [
                {'check_with': check_path},
                {'check_with': check_extension}
            ]  
        },
        'valuesrules': {
            'type': 'dict',
            'allow_unknown': {
              'check_with': check_extension
            },
            'schema': {
                '$ref': {
                  'type': 'string'
                },
                'summary': {
                    'type': 'string'
                },
                'description': {
                    'type': 'string'
                },
                'get': {
                    'type': 'dict',
                    'allow_unknown': {
                      'check_with': check_extension
                    },
                    'schema': {
                        'tags': {
                            'type': 'list',
                            'schema': {
                                'type': 'string'
                            }
                        },
                        'summary': {
                            'type': 'string'
                        },
                        'description': {
                            'type': 'string'
                        },
                        'externalDocs': {
                            'type': 'dict',
                            'allow_unknown': {
                              'check_with': check_extension
                            },
                            'schema': {
                                'description': {
                                    'type': 'string'
                                },
                                'url': {
                                    'required': True,
                                    'type': 'string'
                                }
                            }
                        },
                        'operationId': {
                            'type': 'string'
                        },
                        'parameters': {
                            'type': 'list',
                            'schema': {
                                'anyof': [
                                    {
                                        'type': 'dict',
                                        'schema': {
                                            '$ref': {
                                                'required': True,
                                                'type': 'string'
                                            }
                                        }
                                    },
                                    {
                                        'type': 'dict',
                                        'allow_unknown': {
                                          'check_with': check_extension
                                        },
                                        'schema': {
                                            'name': {
                                                'required': True,
                                                'type': 'string',
                                            },
                                            'in': {
                                                'required': True,
                                                'type': 'string',
                                            },
                                            'description': {
                                                'type': 'string',
                                            },
                                            'required': {
                                                'type': 'boolean',
                                                'default': False,
                                            },
                                            'deprecated': {
                                                'type': 'boolean',
                                                'default': False,
                                            },
                                            'allowEmptyValue': {
                                                'type': 'boolean',
                                                'default': False,
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        'requestBody': {
                            'anyof': [
                                {
                                    'type': 'dict',
                                    'schema': {
                                        '$ref': {
                                            'required': True,
                                            'type': 'string'
                                        }
                                    }
                                },
                                {
                                    'type': 'dict',
                                    'allow_unknown': {
                                      'check_with': check_extension
                                    },
                                    'schema': {
                                        'description': {
                                            'type': 'string',
                                        },
                                        'content': {
                                            'required': True,
                                            'keysrules': {
                                                'type': 'string',
                                                'check_with': check_media_type
                                            },
                                            'valuesrules': {
                                                'type': 'dict',
                                                'allow_unknown': {
                                                    'check_with': check_extension
                                                },
                                                'schema': {
                                                    'schema': {
                                                        'anyof': [
                                                            {
                                                                'type': 'dict',
                                                                'schema': {
                                                                    '$ref': {
                                                                        'required': True,
                                                                        'type': 'string'
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                'type': 'dict',
                                                                'allow_unknown': {
                                                                    'check_with': check_extension
                                                                },
                                                                'schema': {
                                                                    'title': {
                                                                        'type': 'string'
                                                                    },
                                                                    'multipleOf': {
                                                                        'type': 'integer',
                                                                        'min': 1
                                                                    },
                                                                    'maximum': {
                                                                        'type': 'integer'
                                                                    },
                                                                    'exclusiveMaximum': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    },
                                                                    'minimum': {
                                                                        'type': 'integer'
                                                                    },
                                                                    'exclusiveMinimum': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    },
                                                                    'maxLength': {
                                                                        'type': 'integer',
                                                                        'min': 0
                                                                    },
                                                                    'minLength': {
                                                                        'type': 'integer',
                                                                        'min': 0
                                                                    },
                                                                    'pattern': {
                                                                        'type': 'string'
                                                                    },
                                                                    'maxItems': {
                                                                        'type': 'integer',
                                                                        'min': 0
                                                                    },
                                                                    'minItems': {
                                                                        'type': 'integer',
                                                                        'min': 0,
                                                                        'default': 0
                                                                    },
                                                                    'uniqueItems': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    },
                                                                    'maxProperties': {
                                                                        'type': 'integer',
                                                                        'min': 0
                                                                    },
                                                                    'minProperties': {
                                                                        'type': 'integer',
                                                                        'min': 0,
                                                                        'default': 0
                                                                    },
                                                                    'required': {
                                                                        'type': 'list',
                                                                        'minlength': 1,
                                                                        'schema': {
                                                                            'type': 'string'
                                                                        },
                                                                        'check_with': check_list_unique
                                                                    },
                                                                    'enum': {
                                                                        'type': 'list',
                                                                        'minlength': 1,
                                                                        'valuesrules': {
                                                                            'nullable': True
                                                                        }
                                                                    },
                                                                    'type': {
                                                                        'type': 'string'
                                                                    },
                                                                    # allOf, oneOf, anyOf, not, items, additionalProperties, and default are not added due to conplications
                                                                    'allOf': {},
                                                                    'oneOf': {},
                                                                    'anyOf': {},
                                                                    'not': {},
                                                                    'additionalProperties': {},
                                                                    'default': {},
                                                                    'properties': { # restricted to 2 loops
                                                                        'type': 'dict',
                                                                        'keysrules': {
                                                                            'type': 'string'
                                                                        },
                                                                        'valuesrules': {
                                                                            'type': 'dict',
                                                                            'schema': {

                                                                            }
                                                                        }
                                                                    },
                                                                    'description': {
                                                                        'type': 'string'
                                                                    },
                                                                    'format': {
                                                                        'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                                                                    },
                                                                    'nullable': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    },
                                                                    'discriminator': {
                                                                        'type': 'dict',
                                                                        'anyof': [
                                                                            {'dependencies': 'oneOf'},
                                                                            {'dependencies': 'anyOf'},
                                                                            {'dependencies': 'allOf'}
                                                                        ],
                                                                        'schema': {
                                                                            'propertyName': {
                                                                                'required': True,
                                                                                'type': 'string'
                                                                            },
                                                                            'mapping': {
                                                                                'type': 'dict',
                                                                                'keysrules': {
                                                                                    'type': 'string'
                                                                                },
                                                                                'valuesrules': {
                                                                                    'type': 'string'
                                                                                }
                                                                            }
                                                                        }
                                                                    },
                                                                    'readOnly': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    },
                                                                    'writeOnly': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    },
                                                                    'xml': {
                                                                        'type': 'dict',
                                                                        'allow_unknown': {
                                                                            'check_with': check_extension
                                                                        },
                                                                        'schema': {
                                                                            'name': {
                                                                                'type': 'string'
                                                                            },
                                                                            'namespace': {
                                                                                'type': 'string'
                                                                            },
                                                                            'prefix': {
                                                                                'type': 'string'
                                                                            },
                                                                            'attribute': {
                                                                                'type': 'boolean',
                                                                                'default': False
                                                                            },
                                                                            'wrapped': {
                                                                                'type': 'boolean',
                                                                                'default': False
                                                                            }
                                                                        }
                                                                    },
                                                                    'externalDocs': {
                                                                        'type': 'dict',
                                                                        'allow_unknown': {
                                                                            'check_with': check_extension
                                                                        },
                                                                        'schema': {
                                                                            'description': {
                                                                                'type': 'string'
                                                                            },
                                                                            'url': {
                                                                                'required': True,
                                                                                'type': 'string',
                                                                                'check_with': check_url
                                                                            }
                                                                        }
                                                                    },
                                                                    'example': {},
                                                                    'deprecated': {
                                                                        'type': 'boolean',
                                                                        'default': False
                                                                    }
                                                                }
                                                            }
                                                          ],
                                                    # 'example': {},
                                                    # 'examples': {
                                                    #     'type': 'dict',
                                                    #     'keysrules': {
                                                    #         'type': 'string'
                                                    #     },
                                                    #     'valuesrules': {
                                                    #         'anyof': [
                                                    #             {
                                                    #                 'type': 'dict',
                                                    #                 'schema': {
                                                    #                     '$ref': {
                                                    #                         'required': True,
                                                    #                         'type': 'string'
                                                    #                     }
                                                    #                 }
                                                    #             },
                                                    #             {
                                                    #                 'type': 'dict',
                                                    #                 'allow_unknown': {
                                                    #                   'check_with': check_extension
                                                    #                 },
                                                    #                 'schema': {
                                                    #                     'summary': {
                                                    #                         'type': 'string'
                                                    #                     },
                                                    #                     'description': {
                                                    #                         'type': 'string'
                                                    #                     },
                                                    #                     'value': {
                                                    #                         'excludes': 'externalValue'
                                                    #                     },
                                                    #                     'externalValue': {
                                                    #                         'type': 'string',
                                                    #                         'excludes': 'value'
                                                    #                     }
                                                    #                 }
                                                    #             }
                                                    #         ]
                                                    #     }
                                                    # },
                                                    # 'encoding': {
                                                    #     'type': 'dict',
                                                    #     'keysrules': {
                                                    #         'type': 'string'
                                                    #     },
                                                    #     'valuesrules': {
                                                    #         'type': 'dict',
                                                    #         'allow_unknown': {
                                                    #           'check_with': check_extension
                                                    #         },
                                                    #         'schema': {
                                                    #             'contentType': {
                                                    #                 'type': 'string'
                                                    #             },
                                                    #             'headers': {
                                                    #                 'keysrules': {
                                                    #                     'type': 'string'
                                                    #                 },
                                                    #                 'valuesrules': {
                                                    #                     'anyof': [
                                                    #                         {
                                                    #                             'type': 'dict',
                                                    #                             'schema': {
                                                    #                                 '$ref': {
                                                    #                                     'required': True,
                                                    #                                     'type': 'string'
                                                    #                                 }
                                                    #                             }
                                                    #                         },
                                                    #                         {
                                                    #                             'type': 'dict',
                                                    #                             'allow_unknown': {
                                                    #                               'check_with': check_extension
                                                    #                             },
                                                    #                             'schema': {
                                                    #                                 'description': {
                                                    #                                     'type': 'string'
                                                    #                                 },
                                                    #                                 'required': {
                                                    #                                     'required': True,
                                                    #                                     'default': False
                                                    #                                 },
                                                    #                                 'deprecated': {
                                                    #                                     'type': 'boolean',
                                                    #                                     'default': False
                                                    #                                 },
                                                    #                                 'allowEmptyValue': {
                                                    #                                     'type': 'boolean',
                                                    #                                     'default': False
                                                    #                                 },
                                                    #                                 'style': {
                                                    #                                     'type': 'string'
                                                    #                                 },
                                                    #                                 'explode': {
                                                    #                                     'type': 'boolean',
                                                    #                                 },
                                                    #                                 'allowReserved': {
                                                    #                                     'type': 'boolean',
                                                    #                                     'default': False
                                                    #                                 },
                                                    #                                 'schema': {
                                                    #                                     'anyof': [
                                                    #                                         {
                                                    #                                             'type': 'dict',
                                                    #                                             'schema': {
                                                    #                                                 '$ref': {
                                                    #                                                     'required': True,
                                                    #                                                     'type': 'string'
                                                    #                                                 }
                                                    #                                             }
                                                    #                                         },
                                                    #                                         {
                                                    #                                             'type': 'dict',
                                                    #                                             'allow_unknown': {
                                                    #                                                 'check_with': check_extension
                                                    #                                             },
                                                    #                                             'schema': {
                                                    #                                                 'title': {
                                                    #                                                     'type': 'string'
                                                    #                                                 },
                                                    #                                                 'multipleOf': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 1
                                                    #                                                 },
                                                    #                                                 'maximum': {
                                                    #                                                     'type': 'integer'
                                                    #                                                 },
                                                    #                                                 'exclusiveMaximum': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 },
                                                    #                                                 'minimum': {
                                                    #                                                     'type': 'integer'
                                                    #                                                 },
                                                    #                                                 'exclusiveMinimum': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 },
                                                    #                                                 'maxLength': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 0
                                                    #                                                 },
                                                    #                                                 'minLength': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 0
                                                    #                                                 },
                                                    #                                                 'pattern': {
                                                    #                                                     'type': 'string'
                                                    #                                                 },
                                                    #                                                 'maxItems': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 0
                                                    #                                                 },

                                                    #                                                 'minItems': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 0,
                                                    #                                                     'default': 0
                                                    #                                                 },
                                                    #                                                 'uniqueItems': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 },
                                                    #                                                 'maxProperties': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 0
                                                    #                                                 },
                                                    #                                                 'minProperties': {
                                                    #                                                     'type': 'integer',
                                                    #                                                     'min': 0,
                                                    #                                                     'default': 0
                                                    #                                                 },
                                                    #                                                 'required': { # how to check unique?
                                                    #                                                     'type': 'list',
                                                    #                                                     'minlength': 1,
                                                    #                                                     'valuesrules': {
                                                    #                                                         'type': 'string'
                                                    #                                                     }
                                                    #                                                 },
                                                    #                                                 'enum': {
                                                    #                                                     'type': 'list',
                                                    #                                                     'minlength': 1,
                                                    #                                                     'valuesrules': {
                                                    #                                                         'nullable': True
                                                    #                                                     }
                                                    #                                                 },
                                                    #                                                 'type': {
                                                    #                                                     'type': 'string'
                                                    #                                                 },
                                                    #                                                 # allOf, oneOf, anyOf, not, items, additionalProperties, and default are not added due to conplications
                                                    #                                                 'allOf': {},
                                                    #                                                 'oneOf': {},
                                                    #                                                 'anyOf': {},
                                                    #                                                 'not': {},
                                                    #                                                 'additionalProperties': {},
                                                    #                                                 'default': {},
                                                    #                                                 'properties': {
                                                    #                                                     'type': 'dict',
                                                    #                                                     'keysrules': {
                                                    #                                                         'type': 'string'
                                                    #                                                     },
                                                    #                                                     'valuesrules': {
                                                    #                                                         'type': 'dict',
                                                    #                                                         'schema': {
                                                    #                                                             'title': {
                                                    #                                                                 'type': 'string'
                                                    #                                                             },
                                                    #                                                             'multipleOf': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 1
                                                    #                                                             },
                                                    #                                                             'maximum': {
                                                    #                                                                 'type': 'integer'
                                                    #                                                             },
                                                    #                                                             'exclusiveMaximum': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             },
                                                    #                                                             'minimum': {
                                                    #                                                                 'type': 'integer'
                                                    #                                                             },
                                                    #                                                             'exclusiveMinimum': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             },
                                                    #                                                             'maxLength': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 0
                                                    #                                                             },
                                                    #                                                             'minLength': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 0
                                                    #                                                             },
                                                    #                                                             'pattern': {
                                                    #                                                                 'type': 'string'
                                                    #                                                             },
                                                    #                                                             'maxItems': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 0
                                                    #                                                             },

                                                    #                                                             'minItems': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 0,
                                                    #                                                                 'default': 0
                                                    #                                                             },
                                                    #                                                             'uniqueItems': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             },
                                                    #                                                             'maxProperties': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 0
                                                    #                                                             },
                                                    #                                                             'minProperties': {
                                                    #                                                                 'type': 'integer',
                                                    #                                                                 'min': 0,
                                                    #                                                                 'default': 0
                                                    #                                                             },
                                                    #                                                             'required': { # how to check unique?
                                                    #                                                                 'type': 'list',
                                                    #                                                                 'minlength': 1,
                                                    #                                                                 'valuesrules': {
                                                    #                                                                     'type': 'string'
                                                    #                                                                 }
                                                    #                                                             },
                                                    #                                                             'enum': {
                                                    #                                                                 'type': 'list',
                                                    #                                                                 'minlength': 1,
                                                    #                                                                 'valuesrules': {
                                                    #                                                                     'nullable': True
                                                    #                                                                 }
                                                    #                                                             },
                                                    #                                                             'type': {
                                                    #                                                                 'type': 'string'
                                                    #                                                             },
                                                    #                                                             'description': {
                                                    #                                                                 'type': 'string'
                                                    #                                                             },
                                                    #                                                             'format': {
                                                    #                                                                 'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                                                    #                                                             },
                                                    #                                                             'nullable': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             },
                                                    #                                                             'readOnly': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             },
                                                    #                                                             'writeOnly': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             },
                                                    #                                                             'xml': {
                                                    #                                                                 'type': 'dict',
                                                    #                                                                 'allow_unknown': {
                                                    #                                                                     'check_with': check_extension
                                                    #                                                                 },
                                                    #                                                                 'schema': {
                                                    #                                                                     'name': {
                                                    #                                                                         'type': 'string'
                                                    #                                                                     },
                                                    #                                                                     'namespace': {
                                                    #                                                                         'type': 'string'
                                                    #                                                                     },
                                                    #                                                                     'prefix': {
                                                    #                                                                         'type': 'string'
                                                    #                                                                     },
                                                    #                                                                     'attribute': {
                                                    #                                                                         'type': 'boolean',
                                                    #                                                                         'default': False
                                                    #                                                                     },
                                                    #                                                                     'wrapped': {
                                                    #                                                                         'type': 'boolean',
                                                    #                                                                         'default': False
                                                    #                                                                     }
                                                    #                                                                 }
                                                    #                                                             },
                                                    #                                                             'externalDocs': {
                                                    #                                                                 'type': 'dict',
                                                    #                                                                 'allow_unknown': {
                                                    #                                                                     'check_with': check_extension
                                                    #                                                                 },
                                                    #                                                                 'schema': {
                                                    #                                                                     'description': {
                                                    #                                                                         'type': 'string'
                                                    #                                                                     },
                                                    #                                                                     'url': {
                                                    #                                                                         'required': True,
                                                    #                                                                         'type': 'string',
                                                    #                                                                         'check_with': check_url
                                                    #                                                                     }
                                                    #                                                                 }
                                                    #                                                             },
                                                    #                                                             'example': {},
                                                    #                                                             'deprecated': {
                                                    #                                                                 'type': 'boolean',
                                                    #                                                                 'default': False
                                                    #                                                             }
                                                    #                                                         }
                                                    #                                                     }
                                                    #                                                 },
                                                    #                                                 'description': {
                                                    #                                                     'type': 'string'
                                                    #                                                 },
                                                    #                                                 'format': {
                                                    #                                                     'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                                                    #                                                 },
                                                    #                                                 'nullable': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 },
                                                    #                                                 'discriminator': {
                                                    #                                                     'type': 'dict',
                                                    #                                                     'anyof': [
                                                    #                                                         {'dependencies': 'oneOf'},
                                                    #                                                         {'dependencies': 'anyOf'},
                                                    #                                                         {'dependencies': 'allOf'}
                                                    #                                                     ],
                                                    #                                                     'schema': {
                                                    #                                                         'propertyName': {
                                                    #                                                             'required': True,
                                                    #                                                             'type': 'string'
                                                    #                                                         },
                                                    #                                                         'mapping': {
                                                    #                                                             'type': 'dict',
                                                    #                                                             'keysrules': {
                                                    #                                                                 'type': 'string'
                                                    #                                                             },
                                                    #                                                             'valuesrules': {
                                                    #                                                                 'type': 'string'
                                                    #                                                             }
                                                    #                                                         }
                                                    #                                                     }
                                                    #                                                 },
                                                    #                                                 'readOnly': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 },
                                                    #                                                 'writeOnly': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 },
                                                    #                                                 'xml': {
                                                    #                                                     'type': 'dict',
                                                    #                                                     'allow_unknown': {
                                                    #                                                         'check_with': check_extension
                                                    #                                                     },
                                                    #                                                     'schema': {
                                                    #                                                         'name': {
                                                    #                                                             'type': 'string'
                                                    #                                                         },
                                                    #                                                         'namespace': {
                                                    #                                                             'type': 'string'
                                                    #                                                         },
                                                    #                                                         'prefix': {
                                                    #                                                             'type': 'string'
                                                    #                                                         },
                                                    #                                                         'attribute': {
                                                    #                                                             'type': 'boolean',
                                                    #                                                             'default': False
                                                    #                                                         },
                                                    #                                                         'wrapped': {
                                                    #                                                             'type': 'boolean',
                                                    #                                                             'default': False
                                                    #                                                         }
                                                    #                                                     }
                                                    #                                                 },
                                                    #                                                 'externalDocs': {
                                                    #                                                     'type': 'dict',
                                                    #                                                     'allow_unknown': {
                                                    #                                                         'check_with': check_extension
                                                    #                                                     },
                                                    #                                                     'schema': {
                                                    #                                                         'description': {
                                                    #                                                             'type': 'string'
                                                    #                                                         },
                                                    #                                                         'url': {
                                                    #                                                             'required': True,
                                                    #                                                             'type': 'string',
                                                    #                                                             'check_with': check_url
                                                    #                                                         }
                                                    #                                                     }
                                                    #                                                 },
                                                    #                                                 'example': {},
                                                    #                                                 'deprecated': {
                                                    #                                                     'type': 'boolean',
                                                    #                                                     'default': False
                                                    #                                                 }
                                                    #                                             }
                                                    #                                         }
                                                    #                                     ]
                                                    #                                 },
                                                    #                                 'example': {},
                                                    #                                 'examples': {
                                                    #                                     'type': 'dict',
                                                    #                                     'keysrules': {
                                                    #                                         'type': 'string'
                                                    #                                     },
                                                    #                                     'valuesrules': {
                                                    #                                         'anyof': [
                                                    #                                             {
                                                    #                                                 'type': 'dict',
                                                    #                                                 'schema': {
                                                    #                                                     '$ref': {
                                                    #                                                         'required': True,
                                                    #                                                         'type': 'string'
                                                    #                                                     }
                                                    #                                                 }
                                                    #                                             },
                                                    #                                             {
                                                    #                                                 'type': 'dict',
                                                    #                                                 'allow_unknown': {
                                                    #                                                   'check_with': check_extension
                                                    #                                                 },
                                                    #                                                 'schema': {
                                                    #                                                     'summary': {
                                                    #                                                         'type': 'string'
                                                    #                                                     },
                                                    #                                                     'description': {
                                                    #                                                         'type': 'string'
                                                    #                                                     },
                                                    #                                                     'value': {
                                                    #                                                         'excludes': 'externalValue'
                                                    #                                                     },
                                                    #                                                     'externalValue': {
                                                    #                                                         'type': 'string',
                                                    #                                                         'excludes': 'value'
                                                    #                                                     }
                                                    #                                                 }
                                                    #                                             }
                                                    #                                         ]
                                                    #                                     }
                                                    #                                 } # left out content here
                                                    #                             }
                                                    #                         }
                                                    #                     ]
                                                    #                 }
                                                    #             }
                                                    #         },
                                                    #         'style': {
                                                    #             'type': 'string'
                                                    #         },
                                                    #         'explode': {
                                                    #             'type': 'boolean'
                                                    #         },
                                                    #         'allowReserved': {
                                                    #             'type': 'boolean',
                                                    #             'default': False
                                                    #         }
                                                    #     }
                                                    # }
                                                    }
                                                }
                                            }
                                        },
                                        'required': {
                                            'type': 'boolean',
                                            'default': False
                                        }
                                            
                                        }
                                    }
                                ]
                        },
                    }
                }
            }
        }
    }
}
                
                       
                        
                        # 'responses': {
                        #     'required': True,
                        #     'type': 'dict',
                        #     'allow_unknown': {
                        #       'anyof': [{'check_with': check_status_code}, {'check_with': check_extension}]
                        #     },
                        #     'schema': {
                        #         'type': 'dict',
                        #         'allow_unknown': {
                        #           'check_with': check_extension
                        #         },
                        #         'schema': {
                        #             'description': {
                        #                 'required': True,
                        #                 'type': 'string'
                        #             },
                        #             'headers': {
                        #                 'keysrules': {
                        #                     'type': 'string'
                        #                 },
                        #                 'valuesrules': {
                        #                     'anyof': [
                        #                         {
                        #                             'type': 'dict',
                        #                             'schema': {
                        #                                 '$ref': {
                        #                                     'required': True,
                        #                                     'type': 'string'
                        #                                 }
                        #                             }
                        #                         },
                        #                         {
                        #                             'type': 'dict',
                        #                             'allow_unknown': {
                        #                               'check_with': check_extension
                        #                             },
                        #                             'schema': {
                        #                                 'description': {
                        #                                     'type': 'string'
                        #                                 },
                        #                                 'required': {
                        #                                     'required': True,
                        #                                     'default': False
                        #                                 },
                        #                                 'deprecated': {
                        #                                     'type': 'boolean',
                        #                                     'default': False
                        #                                 },
                        #                                 'allowEmptyValue': {
                        #                                     'type': 'boolean',
                        #                                     'default': False
                        #                                 },
                        #                                 'style': {
                        #                                     'type': 'string'
                        #                                 },
                        #                                 'explode': {
                        #                                     'type': 'boolean',
                        #                                 },
                        #                                 'allowReserved': {
                        #                                     'type': 'boolean',
                        #                                     'default': False
                        #                                 },
                        #                                 'schema': {
                        #                                     'anyof': [
                        #                                         {
                        #                                             'type': 'dict',
                        #                                             'schema': {
                        #                                                 '$ref': {
                        #                                                     'required': True,
                        #                                                     'type': 'string'
                        #                                                 }
                        #                                             }
                        #                                         },
                        #                                         {
                        #                                             'type': 'dict',
                        #                                             'allow_unknown': {
                        #                                                 'check_with': check_extension
                        #                                             },
                        #                                             'schema': {
                        #                                                 'title': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'multipleOf': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 1
                        #                                                 },
                        #                                                 'maximum': {
                        #                                                     'type': 'integer'
                        #                                                 },
                        #                                                 'exclusiveMaximum': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'minimum': {
                        #                                                     'type': 'integer'
                        #                                                 },
                        #                                                 'exclusiveMinimum': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'maxLength': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 0
                        #                                                 },
                        #                                                 'minLength': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 0
                        #                                                 },
                        #                                                 'pattern': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'maxItems': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 0
                        #                                                 },

                        #                                                 'minItems': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 0,
                        #                                                     'default': 0
                        #                                                 },
                        #                                                 'uniqueItems': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'maxProperties': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 0
                        #                                                 },
                        #                                                 'minProperties': {
                        #                                                     'type': 'integer',
                        #                                                     'min': 0,
                        #                                                     'default': 0
                        #                                                 },
                        #                                                 'required': { # how to check unique?
                        #                                                     'type': 'list',
                        #                                                     'minlength': 1,
                        #                                                     'valuesrules': {
                        #                                                         'type': 'string'
                        #                                                     }
                        #                                                 },
                        #                                                 'enum': {
                        #                                                     'type': 'list',
                        #                                                     'minlength': 1,
                        #                                                     'valuesrules': {
                        #                                                         'nullable': True
                        #                                                     }
                        #                                                 },
                        #                                                 'type': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 # allOf, oneOf, anyOf, not, items, additionalProperties, and default are not added due to conplications
                        #                                                 'allOf': {},
                        #                                                 'oneOf': {},
                        #                                                 'anyOf': {},
                        #                                                 'not': {},
                        #                                                 'additionalProperties': {},
                        #                                                 'default': {},
                        #                                                 'properties': {
                        #                                                     'type': 'dict',
                        #                                                     'keysrules': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'valuesrules': {
                        #                                                         'type': 'dict',
                        #                                                         'schema': {
                        #                                                             'title': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'multipleOf': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 1
                        #                                                             },
                        #                                                             'maximum': {
                        #                                                                 'type': 'integer'
                        #                                                             },
                        #                                                             'exclusiveMaximum': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'minimum': {
                        #                                                                 'type': 'integer'
                        #                                                             },
                        #                                                             'exclusiveMinimum': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'maxLength': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 0
                        #                                                             },
                        #                                                             'minLength': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 0
                        #                                                             },
                        #                                                             'pattern': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'maxItems': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 0
                        #                                                             },

                        #                                                             'minItems': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 0,
                        #                                                                 'default': 0
                        #                                                             },
                        #                                                             'uniqueItems': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'maxProperties': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 0
                        #                                                             },
                        #                                                             'minProperties': {
                        #                                                                 'type': 'integer',
                        #                                                                 'min': 0,
                        #                                                                 'default': 0
                        #                                                             },
                        #                                                             'required': { # how to check unique?
                        #                                                                 'type': 'list',
                        #                                                                 'minlength': 1,
                        #                                                                 'valuesrules': {
                        #                                                                     'type': 'string'
                        #                                                                 }
                        #                                                             },
                        #                                                             'enum': {
                        #                                                                 'type': 'list',
                        #                                                                 'minlength': 1,
                        #                                                                 'valuesrules': {
                        #                                                                     'nullable': True
                        #                                                                 }
                        #                                                             },
                        #                                                             'type': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'description': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'format': {
                        #                                                                 'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                        #                                                             },
                        #                                                             'nullable': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'readOnly': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'writeOnly': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'xml': {
                        #                                                                 'type': 'dict',
                        #                                                                 'allow_unknown': {
                        #                                                                     'check_with': check_extension
                        #                                                                 },
                        #                                                                 'schema': {
                        #                                                                     'name': {
                        #                                                                         'type': 'string'
                        #                                                                     },
                        #                                                                     'namespace': {
                        #                                                                         'type': 'string'
                        #                                                                     },
                        #                                                                     'prefix': {
                        #                                                                         'type': 'string'
                        #                                                                     },
                        #                                                                     'attribute': {
                        #                                                                         'type': 'boolean',
                        #                                                                         'default': False
                        #                                                                     },
                        #                                                                     'wrapped': {
                        #                                                                         'type': 'boolean',
                        #                                                                         'default': False
                        #                                                                     }
                        #                                                                 }
                        #                                                             },
                        #                                                             'externalDocs': {
                        #                                                                 'type': 'dict',
                        #                                                                 'allow_unknown': {
                        #                                                                     'check_with': check_extension
                        #                                                                 },
                        #                                                                 'schema': {
                        #                                                                     'description': {
                        #                                                                         'type': 'string'
                        #                                                                     },
                        #                                                                     'url': {
                        #                                                                         'required': True,
                        #                                                                         'type': 'string',
                        #                                                                         'check_with': check_url
                        #                                                                     }
                        #                                                                 }
                        #                                                             },
                        #                                                             'example': {},
                        #                                                             'deprecated': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             }
                        #                                                         }
                        #                                                     }
                        #                                                 },
                        #                                                 'description': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'format': {
                        #                                                     'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                        #                                                 },
                        #                                                 'nullable': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'discriminator': {
                        #                                                     'type': 'dict',
                        #                                                     'anyof': [
                        #                                                         {'dependencies': 'oneOf'},
                        #                                                         {'dependencies': 'anyOf'},
                        #                                                         {'dependencies': 'allOf'}
                        #                                                     ],
                        #                                                     'schema': {
                        #                                                         'propertyName': {
                        #                                                             'required': True,
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'mapping': {
                        #                                                             'type': 'dict',
                        #                                                             'keysrules': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'valuesrules': {
                        #                                                                 'type': 'string'
                        #                                                             }
                        #                                                         }
                        #                                                     }
                        #                                                 },
                        #                                                 'readOnly': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'writeOnly': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'xml': {
                        #                                                     'type': 'dict',
                        #                                                     'allow_unknown': {
                        #                                                         'check_with': check_extension
                        #                                                     },
                        #                                                     'schema': {
                        #                                                         'name': {
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'namespace': {
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'prefix': {
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'attribute': {
                        #                                                             'type': 'boolean',
                        #                                                             'default': False
                        #                                                         },
                        #                                                         'wrapped': {
                        #                                                             'type': 'boolean',
                        #                                                             'default': False
                        #                                                         }
                        #                                                     }
                        #                                                 },
                        #                                                 'externalDocs': {
                        #                                                     'type': 'dict',
                        #                                                     'allow_unknown': {
                        #                                                         'check_with': check_extension
                        #                                                     },
                        #                                                     'schema': {
                        #                                                         'description': {
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'url': {
                        #                                                             'required': True,
                        #                                                             'type': 'string',
                        #                                                             'check_with': check_url
                        #                                                         }
                        #                                                     }
                        #                                                 },
                        #                                                 'example': {},
                        #                                                 'deprecated': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 }
                        #                                             }
                        #                                         }
                        #                                     ]
                        #                                 },
                        #                                 'example': {},
                        #                                 'examples': {
                        #                                     'type': 'dict',
                        #                                     'keysrules': {
                        #                                         'type': 'string'
                        #                                     },
                        #                                     'valuesrules': {
                        #                                         'anyof': [
                        #                                             {
                        #                                                 'type': 'dict',
                        #                                                 'schema': {
                        #                                                     '$ref': {
                        #                                                         'required': True,
                        #                                                         'type': 'string'
                        #                                                     }
                        #                                                 }
                        #                                             },
                        #                                             {
                        #                                                 'type': 'dict',
                        #                                                 'allow_unknown': {
                        #                                                   'check_with': check_extension
                        #                                                 },
                        #                                                 'schema': {
                        #                                                     'summary': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'description': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'value': {
                        #                                                         'excludes': 'externalValue'
                        #                                                     },
                        #                                                     'externalValue': {
                        #                                                         'type': 'string',
                        #                                                         'excludes': 'value'
                        #                                                     }
                        #                                                 }
                        #                                             }
                        #                                         ]
                        #                                     }
                        #                                 } # left out content here
                        #                             }
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        #             'content': {
                        #                 'keysrules': {
                        #                     'type': 'string',
                        #                     'check_with': check_media_type
                        #                 },
                        #                 'valuesrules': {
                        #                     'type': 'dict',
                        #                     'allow_unknown': {
                        #                       'check_with': check_extension
                        #                     },
                        #                     'schema': {
                        #                         'schema': {
                        #                             'anyof': [
                        #                                 {
                        #                                     'type': 'dict',
                        #                                     'schema': {
                        #                                         '$ref': {
                        #                                             'required': True,
                        #                                             'type': 'string'
                        #                                         }
                        #                                     }
                        #                                 },
                        #                                 {
                        #                                     'type': 'dict',
                        #                                     'allow_unknown': {
                        #                                         'check_with': check_extension
                        #                                     },
                        #                                     'schema': {
                        #                                         'title': {
                        #                                             'type': 'string'
                        #                                         },
                        #                                         'multipleOf': {
                        #                                             'type': 'integer',
                        #                                             'min': 1
                        #                                         },
                        #                                         'maximum': {
                        #                                             'type': 'integer'
                        #                                         },
                        #                                         'exclusiveMaximum': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         },
                        #                                         'minimum': {
                        #                                             'type': 'integer'
                        #                                         },
                        #                                         'exclusiveMinimum': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         },
                        #                                         'maxLength': {
                        #                                             'type': 'integer',
                        #                                             'min': 0
                        #                                         },
                        #                                         'minLength': {
                        #                                             'type': 'integer',
                        #                                             'min': 0
                        #                                         },
                        #                                         'pattern': {
                        #                                             'type': 'string'
                        #                                         },
                        #                                         'maxItems': {
                        #                                             'type': 'integer',
                        #                                             'min': 0
                        #                                         },

                        #                                         'minItems': {
                        #                                             'type': 'integer',
                        #                                             'min': 0,
                        #                                             'default': 0
                        #                                         },
                        #                                         'uniqueItems': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         },
                        #                                         'maxProperties': {
                        #                                             'type': 'integer',
                        #                                             'min': 0
                        #                                         },
                        #                                         'minProperties': {
                        #                                             'type': 'integer',
                        #                                             'min': 0,
                        #                                             'default': 0
                        #                                         },
                        #                                         'required': { # how to check unique?
                        #                                             'type': 'list',
                        #                                             'minlength': 1,
                        #                                             'valuesrules': {
                        #                                                 'type': 'string'
                        #                                             }
                        #                                         },
                        #                                         'enum': {
                        #                                             'type': 'list',
                        #                                             'minlength': 1,
                        #                                             'valuesrules': {
                        #                                                 'nullable': True
                        #                                             }
                        #                                         },
                        #                                         'type': {
                        #                                             'type': 'string'
                        #                                         },
                        #                                         # allOf, oneOf, anyOf, not, items, additionalProperties, and default are not added due to conplications
                        #                                         'allOf': {},
                        #                                         'oneOf': {},
                        #                                         'anyOf': {},
                        #                                         'not': {},
                        #                                         'additionalProperties': {},
                        #                                         'default': {},
                        #                                         'properties': {
                        #                                             'type': 'dict',
                        #                                             'keysrules': {
                        #                                                 'type': 'string'
                        #                                             },
                        #                                             'valuesrules': {
                        #                                                 'type': 'dict',
                        #                                                 'schema': {
                        #                                                     'title': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'multipleOf': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 1
                        #                                                     },
                        #                                                     'maximum': {
                        #                                                         'type': 'integer'
                        #                                                     },
                        #                                                     'exclusiveMaximum': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     },
                        #                                                     'minimum': {
                        #                                                         'type': 'integer'
                        #                                                     },
                        #                                                     'exclusiveMinimum': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     },
                        #                                                     'maxLength': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 0
                        #                                                     },
                        #                                                     'minLength': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 0
                        #                                                     },
                        #                                                     'pattern': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'maxItems': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 0
                        #                                                     },

                        #                                                     'minItems': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 0,
                        #                                                         'default': 0
                        #                                                     },
                        #                                                     'uniqueItems': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     },
                        #                                                     'maxProperties': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 0
                        #                                                     },
                        #                                                     'minProperties': {
                        #                                                         'type': 'integer',
                        #                                                         'min': 0,
                        #                                                         'default': 0
                        #                                                     },
                        #                                                     'required': { # how to check unique?
                        #                                                         'type': 'list',
                        #                                                         'minlength': 1,
                        #                                                         'valuesrules': {
                        #                                                             'type': 'string'
                        #                                                         }
                        #                                                     },
                        #                                                     'enum': {
                        #                                                         'type': 'list',
                        #                                                         'minlength': 1,
                        #                                                         'valuesrules': {
                        #                                                             'nullable': True
                        #                                                         }
                        #                                                     },
                        #                                                     'type': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'description': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'format': {
                        #                                                         'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                        #                                                     },
                        #                                                     'nullable': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     },
                        #                                                     'readOnly': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     },
                        #                                                     'writeOnly': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     },
                        #                                                     'xml': {
                        #                                                         'type': 'dict',
                        #                                                         'allow_unknown': {
                        #                                                             'check_with': check_extension
                        #                                                         },
                        #                                                         'schema': {
                        #                                                             'name': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'namespace': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'prefix': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'attribute': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             },
                        #                                                             'wrapped': {
                        #                                                                 'type': 'boolean',
                        #                                                                 'default': False
                        #                                                             }
                        #                                                         }
                        #                                                     },
                        #                                                     'externalDocs': {
                        #                                                         'type': 'dict',
                        #                                                         'allow_unknown': {
                        #                                                             'check_with': check_extension
                        #                                                         },
                        #                                                         'schema': {
                        #                                                             'description': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'url': {
                        #                                                                 'required': True,
                        #                                                                 'type': 'string',
                        #                                                                 'check_with': check_url
                        #                                                             }
                        #                                                         }
                        #                                                     },
                        #                                                     'example': {},
                        #                                                     'deprecated': {
                        #                                                         'type': 'boolean',
                        #                                                         'default': False
                        #                                                     }
                        #                                                 }
                        #                                             }
                        #                                         },
                        #                                         'description': {
                        #                                             'type': 'string'
                        #                                         },
                        #                                         'format': {
                        #                                             'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                        #                                         },
                        #                                         'nullable': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         },
                        #                                         'discriminator': {
                        #                                             'type': 'dict',
                        #                                             'anyof': [
                        #                                                 {'dependencies': 'oneOf'},
                        #                                                 {'dependencies': 'anyOf'},
                        #                                                 {'dependencies': 'allOf'}
                        #                                             ],
                        #                                             'schema': {
                        #                                                 'propertyName': {
                        #                                                     'required': True,
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'mapping': {
                        #                                                     'type': 'dict',
                        #                                                     'keysrules': {
                        #                                                         'type': 'string'
                        #                                                     },
                        #                                                     'valuesrules': {
                        #                                                         'type': 'string'
                        #                                                     }
                        #                                                 }
                        #                                             }
                        #                                         },
                        #                                         'readOnly': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         },
                        #                                         'writeOnly': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         },
                        #                                         'xml': {
                        #                                             'type': 'dict',
                        #                                             'allow_unknown': {
                        #                                                 'check_with': check_extension
                        #                                             },
                        #                                             'schema': {
                        #                                                 'name': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'namespace': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'prefix': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'attribute': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 },
                        #                                                 'wrapped': {
                        #                                                     'type': 'boolean',
                        #                                                     'default': False
                        #                                                 }
                        #                                             }
                        #                                         },
                        #                                         'externalDocs': {
                        #                                             'type': 'dict',
                        #                                             'allow_unknown': {
                        #                                                 'check_with': check_extension
                        #                                             },
                        #                                             'schema': {
                        #                                                 'description': {
                        #                                                     'type': 'string'
                        #                                                 },
                        #                                                 'url': {
                        #                                                     'required': True,
                        #                                                     'type': 'string',
                        #                                                     'check_with': check_url
                        #                                                 }
                        #                                             }
                        #                                         },
                        #                                         'example': {},
                        #                                         'deprecated': {
                        #                                             'type': 'boolean',
                        #                                             'default': False
                        #                                         }
                        #                                     }
                        #                                 }
                        #                             ]
                        #                         },
                        #                         'example': {},
                        #                         'examples': {
                        #                             'type': 'dict',
                        #                             'keysrules': {
                        #                                 'type': 'string'
                        #                             },
                        #                             'valuesrules': {
                        #                                 'anyof': [
                        #                                     {
                        #                                         'type': 'dict',
                        #                                         'schema': {
                        #                                             '$ref': {
                        #                                                 'required': True,
                        #                                                 'type': 'string'
                        #                                             }
                        #                                         }
                        #                                     },
                        #                                     {
                        #                                         'type': 'dict',
                        #                                         'allow_unknown': {
                        #                                           'check_with': check_extension
                        #                                         },
                        #                                         'schema': {
                        #                                             'summary': {
                        #                                                 'type': 'string'
                        #                                             },
                        #                                             'description': {
                        #                                                 'type': 'string'
                        #                                             },
                        #                                             'value': {
                        #                                                 'excludes': 'externalValue'
                        #                                             },
                        #                                             'externalValue': {
                        #                                                 'type': 'string',
                        #                                                 'excludes': 'value'
                        #                                             }
                        #                                         }
                        #                                     }
                        #                                 ]
                        #                             }
                        #                         },
                        #                         'encoding': {
                        #                             'type': 'dict',
                        #                             'keysrules': {
                        #                                 'type': 'string'
                        #                             },
                        #                             'valuesrules': {
                        #                                 'type': 'dict',
                        #                                 'allow_unknown': {
                        #                                   'check_with': check_extension
                        #                                 },
                        #                                 'schema': {
                        #                                     'contentType': {
                        #                                         'type': 'string'
                        #                                     },
                        #                                     'headers': {
                        #                                         'keysrules': {
                        #                                             'type': 'string'
                        #                                         },
                        #                                         'valuesrules': {
                        #                                             'anyof': [
                        #                                                 {
                        #                                                     'type': 'dict',
                        #                                                     'schema': {
                        #                                                         '$ref': {
                        #                                                             'required': True,
                        #                                                             'type': 'string'
                        #                                                         }
                        #                                                     }
                        #                                                 },
                        #                                                 {
                        #                                                     'type': 'dict',
                        #                                                     'allow_unknown': {
                        #                                                       'check_with': check_extension
                        #                                                     },
                        #                                                     'schema': {
                        #                                                         'description': {
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'required': {
                        #                                                             'required': True,
                        #                                                             'default': False
                        #                                                         },
                        #                                                         'deprecated': {
                        #                                                             'type': 'boolean',
                        #                                                             'default': False
                        #                                                         },
                        #                                                         'allowEmptyValue': {
                        #                                                             'type': 'boolean',
                        #                                                             'default': False
                        #                                                         },
                        #                                                         'style': {
                        #                                                             'type': 'string'
                        #                                                         },
                        #                                                         'explode': {
                        #                                                             'type': 'boolean',
                        #                                                         },
                        #                                                         'allowReserved': {
                        #                                                             'type': 'boolean',
                        #                                                             'default': False
                        #                                                         },
                        #                                                         'schema': {
                        #                                                             'anyof': [
                        #                                                                 {
                        #                                                                     'type': 'dict',
                        #                                                                     'schema': {
                        #                                                                         '$ref': {
                        #                                                                             'required': True,
                        #                                                                             'type': 'string'
                        #                                                                         }
                        #                                                                     }
                        #                                                                 },
                        #                                                                 {
                        #                                                                     'type': 'dict',
                        #                                                                     'allow_unknown': {
                        #                                                                         'check_with': check_extension
                        #                                                                     },
                        #                                                                     'schema': {
                        #                                                                         'title': {
                        #                                                                             'type': 'string'
                        #                                                                         },
                        #                                                                         'multipleOf': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 1
                        #                                                                         },
                        #                                                                         'maximum': {
                        #                                                                             'type': 'integer'
                        #                                                                         },
                        #                                                                         'exclusiveMaximum': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         },
                        #                                                                         'minimum': {
                        #                                                                             'type': 'integer'
                        #                                                                         },
                        #                                                                         'exclusiveMinimum': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         },
                        #                                                                         'maxLength': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 0
                        #                                                                         },
                        #                                                                         'minLength': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 0
                        #                                                                         },
                        #                                                                         'pattern': {
                        #                                                                             'type': 'string'
                        #                                                                         },
                        #                                                                         'maxItems': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 0
                        #                                                                         },

                        #                                                                         'minItems': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 0,
                        #                                                                             'default': 0
                        #                                                                         },
                        #                                                                         'uniqueItems': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         },
                        #                                                                         'maxProperties': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 0
                        #                                                                         },
                        #                                                                         'minProperties': {
                        #                                                                             'type': 'integer',
                        #                                                                             'min': 0,
                        #                                                                             'default': 0
                        #                                                                         },
                        #                                                                         'required': { # how to check unique?
                        #                                                                             'type': 'list',
                        #                                                                             'minlength': 1,
                        #                                                                             'valuesrules': {
                        #                                                                                 'type': 'string'
                        #                                                                             }
                        #                                                                         },
                        #                                                                         'enum': {
                        #                                                                             'type': 'list',
                        #                                                                             'minlength': 1,
                        #                                                                             'valuesrules': {
                        #                                                                                 'nullable': True
                        #                                                                             }
                        #                                                                         },
                        #                                                                         'type': {
                        #                                                                             'type': 'string'
                        #                                                                         },
                        #                                                                         # allOf, oneOf, anyOf, not, items, additionalProperties, and default are not added due to conplications
                        #                                                                         'allOf': {},
                        #                                                                         'oneOf': {},
                        #                                                                         'anyOf': {},
                        #                                                                         'not': {},
                        #                                                                         'additionalProperties': {},
                        #                                                                         'default': {},
                        #                                                                         'properties': {
                        #                                                                             'type': 'dict',
                        #                                                                             'keysrules': {
                        #                                                                                 'type': 'string'
                        #                                                                             },
                        #                                                                             'valuesrules': {
                        #                                                                                 'type': 'dict',
                        #                                                                                 'schema': {
                        #                                                                                     'title': {
                        #                                                                                         'type': 'string'
                        #                                                                                     },
                        #                                                                                     'multipleOf': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 1
                        #                                                                                     },
                        #                                                                                     'maximum': {
                        #                                                                                         'type': 'integer'
                        #                                                                                     },
                        #                                                                                     'exclusiveMaximum': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     },
                        #                                                                                     'minimum': {
                        #                                                                                         'type': 'integer'
                        #                                                                                     },
                        #                                                                                     'exclusiveMinimum': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     },
                        #                                                                                     'maxLength': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 0
                        #                                                                                     },
                        #                                                                                     'minLength': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 0
                        #                                                                                     },
                        #                                                                                     'pattern': {
                        #                                                                                         'type': 'string'
                        #                                                                                     },
                        #                                                                                     'maxItems': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 0
                        #                                                                                     },

                        #                                                                                     'minItems': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 0,
                        #                                                                                         'default': 0
                        #                                                                                     },
                        #                                                                                     'uniqueItems': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     },
                        #                                                                                     'maxProperties': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 0
                        #                                                                                     },
                        #                                                                                     'minProperties': {
                        #                                                                                         'type': 'integer',
                        #                                                                                         'min': 0,
                        #                                                                                         'default': 0
                        #                                                                                     },
                        #                                                                                     'required': { # how to check unique?
                        #                                                                                         'type': 'list',
                        #                                                                                         'minlength': 1,
                        #                                                                                         'valuesrules': {
                        #                                                                                             'type': 'string'
                        #                                                                                         }
                        #                                                                                     },
                        #                                                                                     'enum': {
                        #                                                                                         'type': 'list',
                        #                                                                                         'minlength': 1,
                        #                                                                                         'valuesrules': {
                        #                                                                                             'nullable': True
                        #                                                                                         }
                        #                                                                                     },
                        #                                                                                     'type': {
                        #                                                                                         'type': 'string'
                        #                                                                                     },
                        #                                                                                     'description': {
                        #                                                                                         'type': 'string'
                        #                                                                                     },
                        #                                                                                     'format': {
                        #                                                                                         'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                        #                                                                                     },
                        #                                                                                     'nullable': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     },
                        #                                                                                     'readOnly': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     },
                        #                                                                                     'writeOnly': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     },
                        #                                                                                     'xml': {
                        #                                                                                         'type': 'dict',
                        #                                                                                         'allow_unknown': {
                        #                                                                                             'check_with': check_extension
                        #                                                                                         },
                        #                                                                                         'schema': {
                        #                                                                                             'name': {
                        #                                                                                                 'type': 'string'
                        #                                                                                             },
                        #                                                                                             'namespace': {
                        #                                                                                                 'type': 'string'
                        #                                                                                             },
                        #                                                                                             'prefix': {
                        #                                                                                                 'type': 'string'
                        #                                                                                             },
                        #                                                                                             'attribute': {
                        #                                                                                                 'type': 'boolean',
                        #                                                                                                 'default': False
                        #                                                                                             },
                        #                                                                                             'wrapped': {
                        #                                                                                                 'type': 'boolean',
                        #                                                                                                 'default': False
                        #                                                                                             }
                        #                                                                                         }
                        #                                                                                     },
                        #                                                                                     'externalDocs': {
                        #                                                                                         'type': 'dict',
                        #                                                                                         'allow_unknown': {
                        #                                                                                             'check_with': check_extension
                        #                                                                                         },
                        #                                                                                         'schema': {
                        #                                                                                             'description': {
                        #                                                                                                 'type': 'string'
                        #                                                                                             },
                        #                                                                                             'url': {
                        #                                                                                                 'required': True,
                        #                                                                                                 'type': 'string',
                        #                                                                                                 'check_with': check_url
                        #                                                                                             }
                        #                                                                                         }
                        #                                                                                     },
                        #                                                                                     'example': {},
                        #                                                                                     'deprecated': {
                        #                                                                                         'type': 'boolean',
                        #                                                                                         'default': False
                        #                                                                                     }
                        #                                                                                 }
                        #                                                                             }
                        #                                                                         },
                        #                                                                         'description': {
                        #                                                                             'type': 'string'
                        #                                                                         },
                        #                                                                         'format': {
                        #                                                                             'allowed': ['int32', 'int64', 'float', 'double', 'byte', 'binary', 'date', 'date-time', 'password']
                        #                                                                         },
                        #                                                                         'nullable': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         },
                        #                                                                         'discriminator': {
                        #                                                                             'type': 'dict',
                        #                                                                             'anyof': [
                        #                                                                                 {'dependencies': 'oneOf'},
                        #                                                                                 {'dependencies': 'anyOf'},
                        #                                                                                 {'dependencies': 'allOf'}
                        #                                                                             ],
                        #                                                                             'schema': {
                        #                                                                                 'propertyName': {
                        #                                                                                     'required': True,
                        #                                                                                     'type': 'string'
                        #                                                                                 },
                        #                                                                                 'mapping': {
                        #                                                                                     'type': 'dict',
                        #                                                                                     'keysrules': {
                        #                                                                                         'type': 'string'
                        #                                                                                     },
                        #                                                                                     'valuesrules': {
                        #                                                                                         'type': 'string'
                        #                                                                                     }
                        #                                                                                 }
                        #                                                                             }
                        #                                                                         },
                        #                                                                         'readOnly': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         },
                        #                                                                         'writeOnly': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         },
                        #                                                                         'xml': {
                        #                                                                             'type': 'dict',
                        #                                                                             'allow_unknown': {
                        #                                                                                 'check_with': check_extension
                        #                                                                             },
                        #                                                                             'schema': {
                        #                                                                                 'name': {
                        #                                                                                     'type': 'string'
                        #                                                                                 },
                        #                                                                                 'namespace': {
                        #                                                                                     'type': 'string'
                        #                                                                                 },
                        #                                                                                 'prefix': {
                        #                                                                                     'type': 'string'
                        #                                                                                 },
                        #                                                                                 'attribute': {
                        #                                                                                     'type': 'boolean',
                        #                                                                                     'default': False
                        #                                                                                 },
                        #                                                                                 'wrapped': {
                        #                                                                                     'type': 'boolean',
                        #                                                                                     'default': False
                        #                                                                                 }
                        #                                                                             }
                        #                                                                         },
                        #                                                                         'externalDocs': {
                        #                                                                             'type': 'dict',
                        #                                                                             'allow_unknown': {
                        #                                                                                 'check_with': check_extension
                        #                                                                             },
                        #                                                                             'schema': {
                        #                                                                                 'description': {
                        #                                                                                     'type': 'string'
                        #                                                                                 },
                        #                                                                                 'url': {
                        #                                                                                     'required': True,
                        #                                                                                     'type': 'string',
                        #                                                                                     'check_with': check_url
                        #                                                                                 }
                        #                                                                             }
                        #                                                                         },
                        #                                                                         'example': {},
                        #                                                                         'deprecated': {
                        #                                                                             'type': 'boolean',
                        #                                                                             'default': False
                        #                                                                         }
                        #                                                                     }
                        #                                                                 }
                        #                                                             ]
                        #                                                         },
                        #                                                         'example': {},
                        #                                                         'examples': {
                        #                                                             'type': 'dict',
                        #                                                             'keysrules': {
                        #                                                                 'type': 'string'
                        #                                                             },
                        #                                                             'valuesrules': {
                        #                                                                 'anyof': [
                        #                                                                     {
                        #                                                                         'type': 'dict',
                        #                                                                         'schema': {
                        #                                                                             '$ref': {
                        #                                                                                 'required': True,
                        #                                                                                 'type': 'string'
                        #                                                                             }
                        #                                                                         }
                        #                                                                     },
                        #                                                                     {
                        #                                                                         'type': 'dict',
                        #                                                                         'allow_unknown': {
                        #                                                                           'check_with': check_extension
                        #                                                                         },
                        #                                                                         'schema': {
                        #                                                                             'summary': {
                        #                                                                                 'type': 'string'
                        #                                                                             },
                        #                                                                             'description': {
                        #                                                                                 'type': 'string'
                        #                                                                             },
                        #                                                                             'value': {
                        #                                                                                 'excludes': 'externalValue'
                        #                                                                             },
                        #                                                                             'externalValue': {
                        #                                                                                 'type': 'string',
                        #                                                                                 'excludes': 'value'
                        #                                                                             }
                        #                                                                         }
                        #                                                                     }
                        #                                                                 ]
                        #                                                             }
                        #                                                         } # left out content here
                        #                                                     }
                        #                                                 }
                        #                                             ]
                        #                                         }
                        #                                     }
                        #                                 },
                        #                                 'style': {
                        #                                     'type': 'string'
                        #                                 },
                        #                                 'explode': {
                        #                                     'type': 'boolean'
                        #                                 },
                        #                                 'allowReserved': {
                        #                                     'type': 'boolean',
                        #                                     'default': False
                        #                                 }
                        #                             }
                        #                         }
                        #                     }
                        #                 }
                        #             },
                        #             'links': {
                        #                 'keysrules': {
                        #                     'type': 'string'
                        #                 },
                        #                 'valuesrules': {
                        #                     'anyof': [
                        #                         {
                        #                             'type': 'dict',
                        #                             'schema': {
                        #                                 '$ref': {
                        #                                     'required': True,
                        #                                     'type': 'string'
                        #                                 }
                        #                             }
                        #                         },
                        #                         {
                        #                             'type': 'dict',
                        #                             'allow_unknown': {
                        #                               'check_with': check_extension
                        #                             },
                        #                             'schema': {
                        #                                 'operationRef': {
                        #                                     'type': 'string',
                        #                                     'excludes': 'operationId'
                        #                                 },
                        #                                 'operationId': {
                        #                                     'type': 'string',
                        #                                     'excludes': 'operationRef'
                        #                                 },
                        #                                 'parameters': {
                        #                                     'type': 'dict',
                        #                                     'keysrules': {
                        #                                         'type': 'string'
                        #                                     }
                        #                                 },
                        #                                 'requestBody': {},
                        #                                 'description': {
                        #                                     'type': 'string'
                        #                                 },
                        #                                 'server': {
                        #                                    'type': 'dict',
                        #                                    'allow_unknown': {
                        #                                       'check_with': check_extension
                        #                                    },
                        #                                    'schema': {
                        #                                        'url': {
                        #                                            'required': True,
                        #                                            'type': 'string'
                        #                                        },
                        #                                        'description': {
                        #                                            'type': 'string'
                        #                                        },
                        #                                        'variables': {
                        #                                            'type': 'dict',
                        #                                            'keysrules': {
                        #                                                'type': 'string'
                        #                                            },
                        #                                            'valuesrules': {
                        #                                                'type': 'dict',
                        #                                                'allow_unknown': {
                        #                                                   'check_with': check_extension
                        #                                                },
                        #                                                'schema': {
                        #                                                    'enum': {
                        #                                                        'type': 'list',
                        #                                                        'schema': {
                        #                                                            'type': 'string'
                        #                                                        }
                        #                                                    },
                        #                                                    'default': {
                        #                                                        'required': True,
                        #                                                        'type': 'string'
                        #                                                    },
                        #                                                    'description': {
                        #                                                        'type': 'string'
                        #                                                    }
                        #                                                }
                        #                                            }
                        #                                        }
                        #                                    } 
                        #                                 }
                        #                             }
                        #                         }
                        #                     ]
                        #                 }
                        #             }
                        #         }
                        #     }
                        # }
                        # 'callbacks': {
                        #     'type': 'dict',
                        #     'keysrules': {
                        #         'type': 'string'
                        #     },
                        #     'valuesrules': {
                        #         'anyof': [
                        #             {
                        #                 'type': 'dict',
                        #                 'schema': {
                        #                     '$ref': {
                        #                         'required': True,
                        #                         'type': 'string'
                        #                     }
                        #                 }
                        #             },
                        #             {
                        #                 'type': 'dict',
                        #                 'allow_unknown': {
                        #                   'check_with': check_extension
                        #                 },
                        #                 'schema': {
                                            
                        #                 }
                        #             }
                        #         ]
                        #     }
                        # },
                        # 'deprecated': {
                        #     'type': 'boolean',
                        #     'default': False
                        # },
                        # 'security': {
                            
                        # },
                        # 'servers': {
                            
                        # }
                #     }
                # }
            # }

        # }
    # }
# }

def flattenDict(d):
    keyValueList = []
    for key, value in d.items():
        if value == None:
            keyValueList.append((key, None))
        else:
            keyValueList.append((key, value))
        if isinstance(value, dict):
            keyValueList.extend(flattenDict(value))
    return keyValueList

def is_key_nested(dictionary, parent_key, nested_key):
    if parent_key in dictionary and nested_key in dictionary[parent_key]:
        return True
    
    for value in dictionary.values():
        if isinstance(value, dict):
            if is_key_nested(value, parent_key, nested_key):
                return True
            elif nested_key in value:
                return True
    
    return False

def getLineNumberFromPath(doc, path):
    if path == "":
        return True
    keysArray = path.split("/")

    for i in range(len(keysArray)):
        for j in range(i, len(keysArray)):
            key = "/".join([keysArray[x] for x in range(i, j + 1)])
            try:
                new_doc = doc[key]
            except:
                continue
            new_keysArray = keysArray.copy()
            new_keysArray = new_keysArray[:i] + new_keysArray[(j + 1):]
            new_path = "/".join(new_keysArray)
            res = getLineNumberFromPath(new_doc, new_path)
            if res == True:
                try:
                    return doc[key].lc.line
                except:
                    return doc.lc.line
            elif res != False:
                return res
    return False

def parse_error(error):
    # Extract the error path using regular expression
    path_regex = r": '([^']*)'"
    path_match = re.search(path_regex, error)
    if path_match:
        error_path = path_match.group(1)
    else:
        error_path = ""

    # Extract the error message by removing the path from the error and some additional processing
    error_message = re.sub(path_regex, "", error).strip()

    # Check if the error message contains enum information
    enum_values = None
    enum_regex = r"Enum: \[(.+)\]"
    enum_match = re.search(enum_regex, error_message)
    if enum_match:
        enum_values = enum_match.group(1)
        error_message = re.sub(enum_regex, "", error_message).strip()


    # Check if the error message contains regex validation error
    regex_string = None
    regex_error_regex = r"Key '(.+)' does not match any regex '(.+)'\."
    regex_error_match = re.search(regex_error_regex, error_message)
    if regex_error_match:
        key = regex_error_match.group(1)
        regex_string = regex_error_match.group(2)
        error_message = f"Key '{key}' invalid value."
    
    # Additional processing
    if "Path ." in error_message:
      error_message = error_message.replace("Path .", "")
    if "Path." in error_message:
      error_message = error_message.replace("Path.", "")
    if "required.novalue" in error_message:
      property = error_path.split("/")[-1]
      error_message = f"Should have required value '{property}'"
    
    # Additional properties that should not be in the doc
    property_match = re.findall(r"Key '([^']*)' was not defined", error_message)
    if property_match:
        additional_property = property_match[0]
        error_message = f"Should not have additional key '{additional_property}'"



    return error_path, error_message, enum_values, regex_string



def main():
  yaml = ruamel.yaml.YAML()
  yaml.Constructor = MyConstructor

  doc_json = yaml.load(doc)


  
  # keyList = keysInNestedDictionary_recursive(doc_json)
  # for key in keyList:
  #     if key == "post":
  #       print(doc_json[key])
  # print(flattenDict(doc_json))

  # if openapi == "" or openapi == None:
  #     for key, value in doc_json.items():
  #       print(key.lc.line)
  # else:
  #     print("missing openapi at line" + str(doc_json["openapi"].lc.line))

  # print(doc_json["openapi"].lc.line)
  # print(doc_json["openapi"].lc.col) # no col for omap keys


  # try:
  #   c = Core(source_data=doc_json, schema_files=["schema1.yaml"])
  #   c.validate()
  # except SchemaError as e:
  #     errors = e.msg
  #     for error in errors.split("\n")[1:]:
  #         error_path, error_message, enum_values, regex_string = parse_error(error)
  #         if regex_string == "^/":
  #             print(error_path)
  #         print("Error Path:", error_path)
  #         print("Error line", getLineNumberFromPath(doc_json, error_path))
  #         print("Error Message:", error_message)
  #         print("Enum values:", enum_values)
  #         print("Error regex string:", regex_string)
  #         print()

  # print(extension('x-author', -1, -1))
  
  v = Validator(schema)
  document = {
      'openapi': '3.0.0',
      'info': {
          'title': 'Update Crediting Status of 55 WDL Application PayNow',
          'description': "This API is to update the crediting status of the member's 55 WDL Application for PayNow",
          'version': '1.0.0',
          'x-author': 'Jennylyn Sze',
          'x-date': '2022-12-22',
      },
      'paths': {
        '/dummy1': {
            'description': "test",
            'get': {
                'tags': ["1", "2"],
                'summary': "lol",
                'description': "wefwejnfe",
                'externalDocs': {
                    'description': "lol",
                    'url': 'http://www.google.com'
                },
                'operationId': "test",
                'parameters': [
                    {
                        '$ref': "test",
                        'name': 'fewfe'
                    }
                ],
                'requestBody': {
                    'description': 'lol',
                    'content': {
                        "application/json": {
                            'schema': {
                                'title': 'test',
                                'multipleOf': 1,
                                'maximum': 10,
                                'exclusiveMaximum': True,
                                'minimum': 10,
                                'exclusiveMinimum': True,
                                'maxLength': 0,
                                'minLength': 0,
                                'pattern': 'test',
                                'maxItems': 0,
                                'minItems': 0,
                                'uniqueItems': True,
                                'maxProperties': 0,
                                'minProperties': 0,
                                'required': ["test1", "test2"]
                            }
                        }
                    },
                    'required': True,
                }
          }
        }
      }
  }
  v.validate(document)
  # print(v.errors)
  for error in v._errors:
      print(error.document_path)


if __name__ == "__main__":
    main()
