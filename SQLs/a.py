import pandas as pd
import yaml
from jinja2 import Template


def get_color(value, column, rules, default_color="white"):
    """Determine cell color based on conditions in YAML."""
    if column in rules:
        for rule in rules[column]:
            for condition, color in rule.items():
                try:
                    if isinstance(value, (int, float)) and isinstance(condition, str):
                        if eval(f"{value} {condition}", {"__builtins__": {}}, {}):
                            return color
                except Exception as e:
                    print(f"Warning: Failed to evaluate condition '{condition}' for value {value} - {e}")
    return default_color  # Default color when no condition matches


def generate_html_table(dfs, yaml_rules):
    """Generate an HTML file with multiple tables from dataframes and YAML rules."""
    rules = yaml.safe_load(yaml_rules)

    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated Tables</title>
    </head>
    <body>
    {% if rules.get('header') %}
        {{ rules['header'] | safe }}
    {% endif %}

    {% for df_name, df in dfs.items() %}
    <h2>{{ df_name }}</h2>
    <table border="1">
        <caption>{% if rules.get(df_name, {}).get('caption') %}{{ rules[df_name]['caption'] }}{% endif %}</caption>
        <tr>
            {% for column in df.columns %}
                <th>{{ column }}</th>
            {% endfor %}
        </tr>
        {% for _, row in df.iterrows() %}
        <tr>
            {% for column in df.columns %}
                {% set color = get_color(row[column], column, rules.get(df_name, {})) %}
                <td style="background-color: {{ color }}">{{ row[column] | e }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    {% endfor %}

    {% if rules.get('trailer') %}
        {{ rules['trailer'] | safe }}
    {% endif %}
    </body>
    </html>
    """)

    return html_template.render(dfs=dfs, get_color=get_color, rules=rules)


# Sample DataFrames
dfs = {
    "Students": pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Marks": [85, 25, 60, 90]
    }),
    "Attendance": pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Attendance": [95, 40, 75, 85]
    })
}

# Updated YAML Formatting Rules with Optional Page Header, Trailer, and Table Captions
yaml_rules = """
header: "<h1>Overall Report</h1>"
trailer: "<h1><em>End of Report.</em></h1>"
Students:
  Marks:
    - ">80": "green"
    - "<30": "red"
Attendance:
  Attendance:
    - ">90": "green"
    - "<50": "red"
  caption: "This table shows attendance records."
"""

# Generate HTML file
html_output = generate_html_table(dfs, yaml_rules)

with open("output_tables.html", "w", encoding="utf-8") as file:
    file.write(html_output)

print("✅ HTML Tables Generated with Conditional Formatting!")
