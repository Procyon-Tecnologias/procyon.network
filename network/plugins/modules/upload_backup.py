#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

import requests


__metaclass__ = type


DOCUMENTATION = """
module: upload_backup
author: Raylan (@jraylan)
short_description: Upload backups files
options:
  url:
    description:
    - URL where the backup files should be uploaded to. The url must accept a
    multipart/form-data. The field name may be set through "field" option.
    type: str
  content:
    description: 
    - The backup file content.
    type: str
  field:
    description:
    - Name of the field of the form-data where the backup files should be
      uploaded
    type: str
    default: "backup"
  filename:
    description:
    - Name of the backup file
    type: str
    default: "backup.cfg"
  extra_data: 
    description:
    - Data to be sent within the request form.
    type: dict[str, str]]
    default: None
  params: 
    description:
    - Parameters to be sent with the request. It may contain the authentication
    credentials or any other required parameter
    type: dict[str, str]]
    default: None
  headers: 
    description:
    - Headers to be sent with the request. It may contain the authentication
    credentials or any other required parameter
    type: dict[str, str]
    default: None
"""

EXAMPLES = """
- name: upload backup files
  procyon.network.upload_backup:
    url: https://example.com/upload_backup/
    filename: backup.cfg
    headers: {
      Authorization: bearer {{ api_token }}
    }
"""

RETURN = """
response_status:
  description: The response status code
  returned: success
  type: int
  sample: 201
exception:
  description: The exception raised if an error occurs
  returned: failure
  type: str
  sample: "Connection to 203.0.113.1 timed out."
"""


from ansible.module_utils.basic import AnsibleModule


def safe(val: str | bytes | None | memoryview):
    if val is None:
        return None

    elif isinstance(val, str):
        return val.encode('utf-8', errors='ignore').decode('utf-8')

    elif isinstance(val, memoryview):
        return val.tobytes().decode('utf-8', errors='ignore')

    return val.decode('utf-8', errors='ignore')


def upload_backup(module: AnsibleModule) -> requests.Response:
    url = module.params['url']
    content = safe(module.params['content'])
    field = module.params.get('field', 'backup')
    filename = module.params.get('filename', 'backup.cfg')
    params = module.params.get('params', {})
    headers = module.params.get('headers', {})
    extra_data = module.params.get('extra_data', {})

    data = {}

    for key, value in extra_data.items():
        data[key] = value

    files = {}
    files[field] = (filename, content)

    return requests.post(
        url,
        data=data,
        files=files,
        headers=headers,
        params=params,
    )


def main():
    """main entry point for execution"""

    argument_spec = dict(
        url=dict(type='str', required=True),
        content=dict(type='str', required=True),
        field=dict(type='str', default='backup'),
        filename=dict(type='str', default='backup.cfg'),
        params=dict(type='dict', default={}),
        headers=dict(type='dict', default={})
    )

    module = AnsibleModule(
      argument_spec=argument_spec,
    )

    result = {
        "response_status": 0,
        "msg": None
    }

    try:
        response = upload_backup(module)
        result["response_status"] = response.status_code
        if response.status_code < 300:
            result['msg'] = response.text
            module.exit_json(**result)
        else:
            module.fail_json(msg=response.text)

    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()