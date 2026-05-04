from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

app = Dash(__name__)

# ---------------------------
# LAYOUT (Task 2.2)
# ---------------------------
app.layout = html.Div([

    html.H1('Automobile Sales Statistics Dashboard',
            style={'textAlign':'center','color':'#503D36','font-size':26}),

    # Dropdown 1: Report Type
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label':'Yearly Statistics','value':'Yearly'},
            {'label':'Recession Period Statistics','value':'Recession'}
        ],
        placeholder='Select a report type',
        value='Yearly'
    ),

    html.Br(),

    # Dropdown 2: Year
    dcc.Dropdown(
        id='select-year',
        options=[{'label':i, 'value':i} for i in sorted(df['Year'].unique())],
        placeholder='Select year',
        value=2010
    ),

    html.Br(),

    # Output container
    html.Div(id='output-container')
])

# ---------------------------
# CALLBACK 1 (Task 2.4)
# Enable/Disable year dropdown
# ---------------------------
@callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_stat):
    if selected_stat == 'Yearly':
        return False
    else:
        return True

# ---------------------------
# CALLBACK 2 (Task 2.5 & 2.6)
# Update graphs
# ---------------------------
@callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(stat_type, year):

    # ---------------------------
    # RECESSION REPORT
    # ---------------------------
    if stat_type == 'Recession':

        recession_data = df[df['Recession'] == 1]

        # Line chart: sales over years
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales',
                       title='Average Automobile Sales during Recession')

        # Bar chart: sales by vehicle type
        rec_bar = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(rec_bar, x='Vehicle_Type', y='Automobile_Sales',
                      title='Average Sales by Vehicle Type (Recession)')

        # Pie chart: advertising expenditure
        rec_pie = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(rec_pie, values='Advertising_Expenditure',
                      names='Vehicle_Type',
                      title='Ad Expenditure Share (Recession)')

        # Bar chart: unemployment vs sales
        rec_unemp = recession_data.groupby('Vehicle_Type')[['Unemployment_Rate','Automobile_Sales']].mean().reset_index()
        fig4 = px.bar(rec_unemp, x='Vehicle_Type', y='Automobile_Sales',
                      color='Unemployment_Rate',
                      title='Unemployment vs Sales')

        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ])

    # ---------------------------
    # YEARLY REPORT
    # ---------------------------
    else:

        yearly_data = df[df['Year'] == year]

        # Line chart: yearly trend
        yearly_trend = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_trend, x='Year', y='Automobile_Sales',
                       title='Yearly Sales Trend')

        # Monthly sales
        monthly = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        fig2 = px.line(monthly, x='Month', y='Automobile_Sales',
                       title=f'Monthly Sales in {year}')

        # Vehicle type sales
        vehicle = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig3 = px.bar(vehicle, x='Vehicle_Type', y='Automobile_Sales',
                      title=f'Vehicle Type Sales in {year}')

        # Pie chart: ad expenditure
        pie = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig4 = px.pie(pie, values='Advertising_Expenditure',
                      names='Vehicle_Type',
                      title=f'Ad Expenditure in {year}')

        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ])


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)