import argparse
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

yaml = YAML(typ="safe")

yaml_output = YAML()
yaml_output.explicit_start = True
yaml_output.default_flow_style = False
yaml_output.indent(sequence=4, offset=2)

def quote_strings(data: Any) -> Any:
    """Double quote value strings in data for YAML."""
    if isinstance(data, str):
        return DoubleQuotedScalarString(data)

    if isinstance(data, list):
        return [quote_strings(item) for item in data]

    if isinstance(data, dict):
        return {key: quote_strings(value) for key, value in data.items()}

    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True)
    parser.add_argument("--intents-dir", required=True)
    args = parser.parse_args()

    lang_code = args.language
    intents_dir = Path(args.intents_dir)

    output_dir = Path('speech_to_phrase/sentences') / lang_code
    output_dir.mkdir(parents=True, exist_ok=True)

    for yaml_file in intents_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            data = yaml.load(f)
        if 'intents' in data:
            merged_data = []
            for intent_key, intent_value in data['intents'].items():
                if 'data' in intent_value:
                    merged_data.extend(intent_value['data'])
            data['data'] = merged_data
            del data['intents']
        output_file = output_dir / yaml_file.name
        with open(output_file, 'w') as f:
            yaml_output.dump(quote_strings(data), f)

if __name__ == '__main__':
    main()