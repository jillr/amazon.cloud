#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by amazon_cloud_code_generator.
# See: https://github.com/ansible-collections/amazon_cloud_code_generator

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: iam_role
short_description: Create and manage EC2 instances
description: Manage EC2 instances (list, create, update, describe, delete).
options:
    assume_role_policy_document:
        description:
        - The trust policy that is associated with this role.
        required: true
        type: dict
    description:
        description:
        - A description of the role that you provide.
        type: str
    managed_policy_arns:
        description:
        - A list of Amazon Resource Names (ARNs) of the IAM managed policies that
            you want to attach to the role.
        elements: str
        type: list
    max_session_duration:
        description:
        - The maximum session duration (in seconds) that you want to set for the specified
            role.
        - If you do not specify a value for this setting, the default maximum of one
            hour is applied.
        - This setting can have a value from 1 hour to 12 hours.
        type: int
    path:
        description:
        - The path to the role.
        type: str
    permissions_boundary:
        description:
        - The ARN of the policy used to set the permissions boundary for the role.
        type: str
    policies:
        description:
        - The inline policy document that is embedded in the specified IAM role.
        elements: dict
        suboptions:
            policy_document:
                description:
                - The policy document.
                required: true
                type: str
            policy_name:
                description:
                - The friendly name (not ARN) identifying the policy.
                required: true
                type: str
        type: list
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        required: false
        type: bool
    role_name:
        description:
        - A name for the IAM role, up to 64 characters in length.
        type: str
    state:
        choices:
        - present
        - absent
        - list
        - describe
        - get
        default: present
        description:
        - Goal state for resouirce.
        - I(state=present) creates the resource if it doesn't exist, or updates to
            the provided state if the resource already exists.
        - I(state=absent) ensures an existing instance is deleted.
        - I(state=list) get all the existing resources.
        - I(state=describe) or I(state=get) retrieves information on an existing resource.
        type: str
    tags:
        aliases:
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        required: false
        type: dict
    wait:
        default: false
        description:
        - Wait for operation to complete before returning.
        type: bool
    wait_timeout:
        default: 320
        description:
        - How many seconds to wait for an operation to complete before timing out.
        type: int
author: Ansible Cloud Team (@ansible-collections)
version_added: 0.0.1
requirements: []
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
"""

EXAMPLES = r"""
"""

RETURN = r"""
result:
    description: Dictionary containing resource information.
    returned: always
    type: complex
    contains:
        identifier:
            description: The unique identifier of the resource.
            type: str
        properties:
            description: The resource properties.
            type: dict
"""

import json

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    CloudControlResource,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    snake_dict_to_camel_dict,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    ansible_dict_to_boto3_tag_list,
)


def main():

    argument_spec = dict(
        state=dict(
            type="str",
            choices=["create", "update", "delete", "list", "describe", "get"],
            default="create",
        ),
    )

    argument_spec["assume_role_policy_document"] = {"type": "dict", "required": True}
    argument_spec["description"] = {"type": "str"}
    argument_spec["managed_policy_arns"] = {"type": "list", "elements": "str"}
    argument_spec["max_session_duration"] = {"type": "int"}
    argument_spec["path"] = {"type": "str"}
    argument_spec["permissions_boundary"] = {"type": "str"}
    argument_spec["policies"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "policy_document": {"type": "str", "required": True},
            "policy_name": {"type": "str", "required": True},
        },
    }
    argument_spec["role_name"] = {"type": "str"}
    argument_spec["tags"] = {
        "type": "dict",
        "required": False,
        "aliases": ["resource_tags"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["purge_tags"] = {"type": "bool", "required": False, "default": True}

    required_if = [
        ["state", "create", ["role_name", "assume_role_policy_document"], True],
        ["state", "update", ["role_name"], True],
        ["state", "delete", ["role_name"], True],
        ["state", "get", ["role_name"], True],
    ]

    module = AnsibleAWSModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::IAM::Role"

    params = {}

    params["assume_role_policy_document"] = module.params.get(
        "assume_role_policy_document"
    )
    params["description"] = module.params.get("description")
    params["managed_policy_arns"] = module.params.get("managed_policy_arns")
    params["max_session_duration"] = module.params.get("max_session_duration")
    params["path"] = module.params.get("path")
    params["permissions_boundary"] = module.params.get("permissions_boundary")
    params["policies"] = module.params.get("policies")
    params["role_name"] = module.params.get("role_name")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags", None):
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ["path", "role_name"]

    state = module.params.get("state")
    identifier = module.params.get("role_name")

    results = {"changed": False, "result": []}

    if state == "list":
        results["result"] = cloud.list_resources(type_name)

    if state in ("describe", "get"):
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "present":
        results["changed"] |= cloud.present(
            type_name, identifier, params_to_set, create_only_params
        )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "absent":
        results["changed"] |= cloud.delete_resource(type_name, identifier)

    module.exit_json(**results)


if __name__ == "__main__":
    main()