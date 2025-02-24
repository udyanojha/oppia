# Copyright 2021 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS-IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script for extending index.yaml.
In Python 2, the index.yaml autoamtically extended with # AUTOGENERATED,
but this is no longer true in Python 3.

This script extracts new kind from
../cloud_datastore_emulator_cache/WEB-INF/index.yaml
and appends it into index.yaml"""

from __future__ import annotations

import copy
import os

import yaml

INDEX_YAML_PATH = os.path.join(os.getcwd(), 'index.yaml')
WEB_INF_INDEX_YAML_PATH = os.path.join(
    os.getcwd(), '..', 'cloud_datastore_emulator_cache', 'WEB-INF', 'index.yaml'
)


def main() -> None:
    """Extends index.yaml file."""
    with open(INDEX_YAML_PATH, 'r', encoding='utf-8') as f:
        index_yaml_dict = yaml.safe_load(f)
    with open(WEB_INF_INDEX_YAML_PATH, 'r', encoding='utf-8') as f:
        web_inf_index_yaml_dict = yaml.safe_load(f)

    if web_inf_index_yaml_dict['indexes'] is None:
        return

    # There is a possibility that an index in index.yaml may exist in
    # ../cloud_datastore_emulator_cache/WEB-INF/index.yaml with different
    # order of properties. We don't need to append those indexes. So we will
    # compare sorted dictionaries. Deepcopy is used here to avoid changing the
    # order of index_yaml_dict after sorting temp_index_yaml_dict.
    temp_index_yaml_dict = copy.deepcopy(index_yaml_dict)
    for kind in temp_index_yaml_dict['indexes']:
        kind['properties'] = sorted(
            kind['properties'], key=lambda x: x['name']
    )

    new_kinds = []
    for kind in web_inf_index_yaml_dict['indexes']:
        # Deepcopy is used here to avoid changing the order of kind in
        # temp_index_yaml_dict after sorting temp_web_inf_kind.
        temp_web_inf_kind = copy.deepcopy(kind)
        temp_web_inf_kind['properties'] = sorted(
            temp_web_inf_kind['properties'], key=lambda x: x['name'])
        if temp_web_inf_kind not in temp_index_yaml_dict['indexes']:
            new_kinds.append(kind)

    if len(new_kinds) == 0:
        return

    index_yaml_dict['indexes'] += new_kinds
    # The yaml dump function doesn't add new lines between kinds
    # automatically. So we add new lines manually using replace
    # function.
    new_index_yaml_dict = yaml.safe_dump(
        index_yaml_dict, default_flow_style=False, sort_keys=False
    )
    index_yaml = new_index_yaml_dict.replace('- kind', '\n- kind')
    with open(INDEX_YAML_PATH, 'w', encoding='utf-8') as f:
        f.write(index_yaml)
