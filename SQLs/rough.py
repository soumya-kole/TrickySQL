import pandas as pd

# Sample DataFrame for the main table
data_main = {
    'TableName': ['Table1', 'Table2', 'Table3'],
    'Number of Rules': [5, 3, 4],
    'Rule Passed': [5, 2, 0],
    'Rules Failed': [0, 1, 4]
}
df_main = pd.DataFrame(data_main)

# Sample DataFrame for rules and status
data_status = {
    'rule': ['rule1', 'rule2', 'rule3', 'rule4', 'rule5'],
    'status': ['passed', 'passed', 'passed', 'passed', 'passed']
}
df_status = pd.DataFrame(data_status)



import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Sample DataFrame for the main table
data_main = {
    'TableName': ['Table1', 'Table2', 'Table3'],
    'Number of Rules': [5, 3, 4],
    'Rule Passed': [5, 2, 0],
    'Rules Failed': [0, 1, 4]
}
df_main = pd.DataFrame(data_main)

# Sample DataFrame for rules and status
data_status = {
    'rule': ['rule1', 'rule2', 'rule3', 'rule4', 'rule5'],
    'status': ['passed', 'failed', 'passed', 'passed', 'passed']
}
df_status = pd.DataFrame(data_status)

# Filter for failed rules
failed_rules = df_status[df_status['status'] == 'failed']
print(failed_rules)

# Convert DataFrame to a list of dictionaries
data_main_dict = df_main.to_dict(orient='records')
data_status_dict = failed_rules.to_dict(orient='records') if not failed_rules.empty else None

# Load the Jinja2 template
file_loader = FileSystemLoader('/Users/soumya/Downloads/')
env = Environment(loader=file_loader)
template = env.get_template('template.html')

# Render the template with data
output = template.render(data_main=data_main_dict, data_status=data_status_dict)

# Save the rendered HTML to a file
with open('output.html', 'w') as f:
    f.write(output)

print("HTML file has been created: output.html")
