import inspect
from pathlib import Path
import re

from neuralake.core import (
    Catalog,
    Filter,
    ModuleDatabase,
    NlkDataFrame,
    ParquetTable,
    Partition,
    PartitioningScheme,
    table,
)

# List of classes and functions to document
things_to_document = {
    "ParquetTable": ParquetTable,
    "Filter": Filter,
    "table": table,
    "NlkDataFrame": NlkDataFrame,
    "Partition": Partition,
    "PartitioningScheme": PartitioningScheme,
    "Catalog": Catalog,
    "ModuleDatabase": ModuleDatabase,
}

# Directory to save the documentation
project_root = Path(__file__).parent.parent
output_dir = project_root / "docs" / "api_reference"
output_dir.mkdir(parents=True, exist_ok=True)


def get_clean_doc(obj):
    """Gets a cleaned docstring for an object."""
    doc = inspect.getdoc(obj)
    return doc.strip() if doc else ""


def format_signature(name, obj):
    """Format a clean function/method signature."""
    try:
        signature = inspect.signature(obj)
        return f"def {name}{signature}:"
    except (ValueError, TypeError):
        return f"def {name}(...):"


def parse_docstring(docstring):
    """Parse a docstring to extract description and parameters while preserving code examples."""
    if not docstring:
        return "", []

    lines = docstring.split("\n")
    description_lines = []
    parameters = []
    current_section = "description"
    current_param = None
    in_code_block = False

    for _, line in enumerate(lines):
        original_line = line
        line = line.strip()

        # Detect ASCII tables or code examples (lines with multiple pipes, arrows, or specific patterns)
        is_ascii_art = (
            "|" in line
            and line.count("|") >= 2
            or ">>>" in line
            or "---" in line
            and len(line) > 10
            or line.startswith("shape:")
            or re.match(r"^\s*[│┌┐└┘├┤┬┴┼─═║╔╗╚╝╠╣╦╩╬]", original_line)
            or (line and all(c in "|-+═│┌┐└┘├┤┬┴┼ " for c in line))
        )

        # Check if we're entering or in a code block
        if is_ascii_art or ">>>" in line:
            if not in_code_block:
                # Start a code block
                if current_section == "description":
                    description_lines.append("")
                    description_lines.append("```")
                in_code_block = True

            # Add the line with original indentation preserved
            if current_section == "description":
                description_lines.append(original_line.rstrip())
            continue

        # Check if we should end a code block
        if in_code_block and line and not is_ascii_art and ">>>" not in line:
            # End the code block
            if current_section == "description":
                description_lines.append("```")
                description_lines.append("")
            in_code_block = False

        # Check if this is a parameter line
        param_match = re.match(r"^(\w+)\s*:\s*(.+)", line)
        if param_match and not in_code_block:
            # End any open code block
            if in_code_block and current_section == "description":
                description_lines.append("```")
                description_lines.append("")
                in_code_block = False

            # Save previous parameter if exists
            if current_param:
                parameters.append(current_param)

            param_name, param_desc = param_match.groups()
            current_param = {"name": param_name, "description": [param_desc]}
            current_section = "parameter"
            continue

        # Check if this is a continuation of parameter description
        if (
            current_section == "parameter"
            and line
            and not line.startswith("Parameters")
            and not line.startswith("Returns")
            and not in_code_block
        ):
            if current_param:
                current_param["description"].append(line)
            continue

        # Check for section headers
        if (
            line.lower() in ["parameters", "parameters:", "args:", "arguments:"]
            and not in_code_block
        ):
            # End any open code block
            if in_code_block and current_section == "description":
                description_lines.append("```")
                description_lines.append("")
                in_code_block = False
            current_section = "parameters_header"
            continue
        elif line.lower() in ["returns", "returns:", "return:"] and not in_code_block:
            # End any open code block
            if in_code_block and current_section == "description":
                description_lines.append("```")
                description_lines.append("")
                in_code_block = False
            # Save last parameter if exists
            if current_param:
                parameters.append(current_param)
                current_param = None
            current_section = "returns"
            continue

        # Add to description if we're in description section
        if current_section == "description" and not in_code_block:
            description_lines.append(line)

    # Close any open code block
    if in_code_block and current_section == "description":
        description_lines.append("```")

    # Save last parameter if exists
    if current_param:
        parameters.append(current_param)

    # Clean up description
    description = "\n".join(description_lines).strip()

    # Clean up parameter descriptions
    for param in parameters:
        param["description"] = " ".join(param["description"]).strip()

    return description, parameters


def format_parameters(parameters):
    """Format parameters into readable Markdown."""
    if not parameters:
        return []

    lines = []
    lines.append("### Parameters")
    lines.append("")

    for param in parameters:
        # Extract type information if present
        desc = param["description"]
        type_match = re.match(r"^([^,]+),?\s*(.*)$", desc)

        if type_match:
            type_info = type_match.group(1).strip()
            remaining_desc = type_match.group(2).strip()

            lines.append(f"- **`{param['name']}`** (*{type_info}*)")
            if remaining_desc:
                lines.append(f"  {remaining_desc}")
        else:
            lines.append(f"- **`{param['name']}`**")
            if desc:
                lines.append(f"  {desc}")
        lines.append("")

    return lines


def generate_docs_for_object(name, obj):
    """Generates clean Markdown documentation for a given Python object."""
    lines = []

    try:
        if inspect.isclass(obj):
            # Class header
            lines.append(f"# API Reference: `{name}`")
            lines.append("")

            # Class docstring
            class_doc = get_clean_doc(obj)
            if class_doc:
                description, parameters = parse_docstring(class_doc)
                if description:
                    lines.append(description)
                    lines.append("")

                if parameters:
                    lines.extend(format_parameters(parameters))

            # Class signature (constructor)
            try:
                init_method = getattr(obj, "__init__", None)
                if init_method and init_method != object.__init__:
                    lines.append("## Constructor")
                    lines.append("")
                    lines.append("```python")
                    lines.append(format_signature("__init__", init_method))
                    lines.append("```")
                    lines.append("")

                    init_doc = get_clean_doc(init_method)
                    if init_doc:
                        description, parameters = parse_docstring(init_doc)
                        if description:
                            lines.append(description)
                            lines.append("")

                        if parameters:
                            lines.extend(format_parameters(parameters))
            except Exception:
                pass

            # Get all public methods (excluding __init__ since we handled it above)
            methods = inspect.getmembers(obj, predicate=inspect.ismethod)
            functions = inspect.getmembers(obj, predicate=inspect.isfunction)
            all_methods = methods + functions

            public_methods = [
                (method_name, method_obj)
                for method_name, method_obj in all_methods
                if not method_name.startswith("_")
                or method_name in ["__call__", "__str__", "__repr__"]
            ]

            if public_methods:
                lines.append("## Methods")
                lines.append("")

                for method_name, method_obj in sorted(public_methods):
                    lines.append(f"### `{method_name}`")
                    lines.append("")

                    # Method signature
                    lines.append("```python")
                    lines.append(format_signature(method_name, method_obj))
                    lines.append("```")
                    lines.append("")

                    # Method documentation
                    method_doc = get_clean_doc(method_obj)
                    if method_doc:
                        description, parameters = parse_docstring(method_doc)
                        if description:
                            lines.append(description)
                            lines.append("")

                        if parameters:
                            lines.extend(format_parameters(parameters))
                    else:
                        lines.append("*No documentation available.*")
                        lines.append("")

        elif inspect.isfunction(obj):
            # Function header
            lines.append(f"# API Reference: `{name}`")
            lines.append("")

            # Function signature
            lines.append("```python")
            lines.append(format_signature(name, obj))
            lines.append("```")
            lines.append("")

            # Function documentation
            func_doc = get_clean_doc(obj)
            if func_doc:
                description, parameters = parse_docstring(func_doc)
                if description:
                    lines.append(description)
                    lines.append("")

                if parameters:
                    lines.extend(format_parameters(parameters))
            else:
                lines.append("*No documentation available.*")
                lines.append("")

        else:
            # Fallback for other object types
            lines.append(f"# API Reference: `{name}`")
            lines.append("")
            lines.append(f"**Type:** `{type(obj).__name__}`")
            lines.append("")

            doc = get_clean_doc(obj)
            if doc:
                description, parameters = parse_docstring(doc)
                if description:
                    lines.append(description)
                    lines.append("")

                if parameters:
                    lines.extend(format_parameters(parameters))
            else:
                lines.append("*No documentation available.*")
                lines.append("")

        # Join all lines with actual newlines
        return "\n".join(lines)

    except Exception as e:
        print(f"  - Error processing {name}: {e}")
        return None


# Generate and save the documentation for each item
for name, obj in things_to_document.items():
    output_path = output_dir / f"{name}.md"
    print(f"Generating docs for {name} -> {output_path.relative_to(project_root)}")

    md_content = generate_docs_for_object(name, obj)

    if md_content:
        with output_path.open("w", encoding="utf-8") as f:
            f.write(md_content)

print("\nDocumentation generation complete.")
print(f"Files are saved in the '{output_dir.relative_to(project_root)}' directory.")
