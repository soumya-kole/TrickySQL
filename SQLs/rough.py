<!DOCTYPE html>
<html>
<head>
    <style>
        .header {
            background-color: blue;
            color: white;
        }
        .success { background-color: green; color: white; }
        .failure { background-color: red; color: white; }
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            padding: 8px;
        }
        a {
            color: blue;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr class="header">
                <th>SRC</th>
                <th>TGT</th>
                <th>RESULT</th>
                <th>ROWS_COMPARED</th>
                <th>COLUMNS_COMPARED</th>
                <th>SAMPLE_MISMATCH</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                <td>{{ row.SRC }}</td>
                <td>{{ row.TGT }}</td>
                <td class="{{ 'success' if row.RESULT == 'SUCCESS' else 'failure' }}">{{ row.RESULT }}</td>
                <td>{{ row.ROWS_COMPARED }}</td>
                <td>{{ row.COLUMNS_COMPARED }}</td>
                <td><a href="file://{{ row.SAMPLE_MISMATCH }}" target="_blank">{{ row.SAMPLE_MISMATCH }}</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>




import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Sample DataFrame
data = {
    'SRC': ['src1', 'src2', 'src3'],
    'TGT': ['tgt1', 'tgt2', 'tgt3'],
    'RESULT': ['SUCCESS', 'FAILURE', 'SUCCESS'],
    'ROWS_COMPARED': [100, 150, 200],
    'COLUMNS_COMPARED': [10, 15, 20],
    'SAMPLE_MISMATCH': ['/Users/soumya/Technicals/Notebooks/table_template.html', '/Users/soumya/Technicals/Notebooks/tutorial-great-expectations/data/avocado.csv', '/path/to/file3']
}

df = pd.DataFrame(data)

# Load the template
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template('table_template.html')

# Render the template with the DataFrame
html_output = template.render(rows=df.to_dict(orient='records'))

# Save the output to a file
with open('report.html', 'w') as file:
    file.write(html_output)

print("HTML report generated successfully!")
