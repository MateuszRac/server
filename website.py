import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Generate data for linear plot
x = [i for i in range(10)]
y = [2 * i + 5 for i in x]

# Create an interactive plot
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Linear Plot'))
fig.update_layout(title='Interactive Linear Plot', xaxis_title='X-axis', yaxis_title='Y-axis')

# Save the plot as an HTML file
html_file_path = '/var/www/index.html'
fig.write_html(html_file_path)

print(f"Interactive HTML file saved at: {html_file_path}")
