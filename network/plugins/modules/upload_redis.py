#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

import redis


__metaclass__ = type


DOCUMENTATION = """
module: upload_redis
author: Raylan (@jraylan)
short_description: Upload backups files to Redis
description:
    - Upload backups files to Redis.
      Requires redis to be installed `pip install redis`.
options:
  host:
    description:
    - Hostname of the Redis server
    type: str
    default: "localhost"
  port:
    description:
    - Port of the Redis server
    type: int
    default: 6379
  db:
    description:
    - Port of the Redis server
    type: int
    default: 1
  name:
    description:
    - The Redis key
    type: str
  content:
    description: 
    - The backup file content.
    type: str
  redis_command:
    description:
    - Redis command to be executed.
      The options are: xadd, set, lpush,  rpush.
    type: str
    default: "set"
"""

EXAMPLES = """
- name: upload backup files
  procyon.network.upload_redis:
    host: 'localhost'
    port: 6379
    db: 3
    name: "example:foo"
    content: "foo bar"
"""

RETURN = """
code:
  description: The code returned by Redis
  returned: always
  type: int
  sample: 1
exception:
  description: The exception raised if an error occurs
  returned: failure
  type: str
  sample: "Connection to localhost timed out."
"""


from ansible.module_utils.basic import AnsibleModule


def upload_backup(module: AnsibleModule) -> int:
    host = module.params['host']
    port = module.params['port']
    db = module.params['db']
    name = module.params['name']
    content = module.params['content']
    redis_command = module.params['redis_command']
    data = {}
    
    client = redis.Redis(
        host=host,
        port=port,
        db=db,
    )

    if 'xadd' == redis_command:
        result = client.xadd(name, {'content': content})
      
    elif 'set' == redis_command:
        result = client.set(name, content)
      
    elif 'lpush' == redis_command:
        result = client.lpush(name, content)
      
    elif 'rpush' == redis_command:
        result = client.rpush(name, content)
    else:
        raise ValueError('Unknown redis command "%".' % redis_command)
      
    return result # type: ignore


def main():
    """main entry point for execution"""

    argument_spec=dict(
        host=dict(type='str', default='localhost'),
        port=dict(type='int', default=6379),
        db=dict(type='str', default=1),
        name=dict(type='str', required=True),
        content=dict(type='str', required=True),
        redis_command=dict(
            type='str', default="set",
            choices=['xadd', 'set', 'lpush', 'rpush']))
    

    module = AnsibleModule(
    argument_spec=argument_spec,
    )

    result = {
        "code": 0
    }    

    try:
        result["response_status"] = upload_backup(module)
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
