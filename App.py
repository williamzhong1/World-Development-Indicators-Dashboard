import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3

import time
start_time = time.time()

#database.sqlite must be in same directory
conn = sqlite3.connect("database.sqlite")

df = pd.read_sql('''
                SELECT c.ShortName, c.CountryCode, i.IndicatorCode, i.IndicatorName, i.Value, i.Year
                FROM Indicators AS i
                INNER JOIN Country AS c
                ON c.CountryCode = i.CountryCode
                WHERE i.IndicatorCode = 'SP.DYN.LE00.IN'
                OR i.IndicatorCode = 'NY.GDP.PCAP.CD'
                OR i.IndicatorCode = 'EN.ATM.CO2E.KT'
                OR i.IndicatorCode = 'EN.ATM.CO2E.PC'
                OR i.IndicatorCode = 'EN.ATM.CO2E.GF.ZS'
                OR i.IndicatorCode = 'EN.ATM.CO2E.LF.ZS'
                OR i.IndicatorCode = 'EN.ATM.CO2E.LF.KT'
                OR i.IndicatorCode = 'EN.ATM.CO2E.SF.ZS'
                ''', con = conn)

print("SQL Query competed in" + "--- %s seconds ---" % (time.time() - start_time))



app = dash.Dash()


app.layout = html.Div([
    html.H1(children = "World Development Indicators"),
    html.Div(
        children = "Visualisations using World Development Indicators Data", style = {"padding-bottom" : "60px"}
    ),
    html.Div([
    dcc.Dropdown(
            id = "year-drop",
            options = [
                {"label" : str(year), "value" : int(year)} for year in df["Year"].unique()
                ],
            value = 2000
        ),
        dcc.Graph(id = "graph-with-slider"),

    ], style = {"margin-bottom" : "60px"}),
    html.Div(children = "Life Expectancy and GDP is a common indicator of human welfare. There are several notable trends. " +
                        "First is the shape of the graph. " + "There appears to be a inverse square relationship, where the trend line cutting through the data curves toward an asymptote. " +
                        "This is interesting because it suggests that no matter the GDP-Per Capita, all countries will run against a hard limit where they can no longer improve life expectancy. "
                        "The hard limit is most likely set by limits to which health technology can improve life expectancy. " +
                        "Second is the fact that the hard limit discussed previously has shifted over the past decades, increasing with the wider availability and growth in " +
                        "health technologies. Use the dropdown menu to select a year. " + "Finally, the last interesting trend is that higher GDP per capita doesn't neccesarily improve " +
                        "life expectancy by such a significant degree.  " + "Comparing data points on the upper right corner of the graph with the large grouping of data points toward the left upper corner " +
                        "reveals that the difference in life expectancy is not significant. This phenomenon may simply be because, even with technology, individuals are aging to the point where even health-care cannot " +
                        "assist, even with additional spending (higher GDP)."

            , style = {"margin-bottom" : "60px", "fontsize" : "20px"}),
    html.Div([
        dcc.Dropdown(
            id = "country-drop",
            options = [
                {"label" : str(name), "value" : str(name)} for name in df["ShortName"].unique()
            ],
            value = "Afghanistan",
        )
        ], style = {"width" : "100%", "margin-bottom" : "60px"}),

    html.Div([
            dcc.Graph(id = "CO2-Fill"),
    ]
    ,style = {"width" : "50%", "display" : "inline-block"}
    ),
    html.Div([
        dcc.Graph(id="CO2-Overall")
    ]
    , style = {"width" : "50%", "display" : "inline-block"}
    ),
html.Div(children = "Note: the stacked bar chart on the left will not add up to 100% for some countries because of missing data. " +
                    "Hover over graph to read indicators. " + "Notable trends: Across different countries, there has been an increase " +
                    "in gaseous forms of fossil fuels and there has been an overall increase on C02 emissions from all countries. "

            , style = {"margin-bottom" : "60px", "fontsize" : "20px"}),


], style = {"padding" : "60px"})

@app.callback(
    dash.dependencies.Output("graph-with-slider", "figure"),
    [dash.dependencies.Input("year-drop", "value")])
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]
    traces = []
    for i in filtered_df["ShortName"].unique():
        df_by_country = filtered_df[filtered_df["ShortName"] == i]
        traces.append(go.Scatter(
            x = df_by_country.loc[df_by_country.IndicatorCode == "NY.GDP.PCAP.CD"]["Value"],
            y = df_by_country.loc[df_by_country.IndicatorCode == "SP.DYN.LE00.IN"]["Value"],
            text = df_by_country["ShortName"],
            mode = "markers",
            opacity = 0.7,
            marker = {
                "size" : 15,
                "line" : {"width" : 0.5, "color" : "white"}
            },
            name = i
        )
)
    return {
        "data" : traces,
        "layout" : go.Layout(
            xaxis = {"type" : "linear", "title" : "GDP Per Capita"},
            yaxis = {"title" : "Life Expectancy"},
            margin = {"l" : 40, "b" : 40, "t" : 10, "r" : 10},
            hovermode = "closest"
        )
    }

@app.callback(
    dash.dependencies.Output("CO2-Fill", "figure"),
    [dash.dependencies.Input("country-drop", "value")]
)
def update_figure1(selected_country):
    filtered_df1 = df[df.IndicatorCode.isin(["EN.ATM.CO2E.GF.ZS", "EN.ATM.CO2E.LF.ZS", "EN.ATM.CO2E.SF.ZS"])]
    filtered_df1_byCountry = filtered_df1[filtered_df1.ShortName == selected_country]
    traces1 = []
    for i in filtered_df1.IndicatorCode.unique():
        traces1.append(go.Bar(
        x = filtered_df1_byCountry.loc[filtered_df1.IndicatorCode == i]["Year"].tolist(),
        y = filtered_df1_byCountry.loc[filtered_df1.IndicatorCode == i]["Value"].tolist(),
        text = filtered_df1_byCountry.loc[filtered_df1.IndicatorCode == i]["IndicatorName"],
#        mode = "markers",
#        opacity = 0.7,
#        marker = {
#                     "size": 15,
#                     "line": {"width": 0.5, "color": "white"}
#                 },
        name = i,
        ))
    return {
        "data" : traces1,
        "layout": go.Layout(
            xaxis={"type": "linear", "title": "Year"},
            yaxis={"title": "CO2 Emissions"},
            margin={"l": 40, "b": 40, "t": 10, "r": 10},
            hovermode="closest",
            barmode = "stack",
            showlegend = False
        )
    }


@app.callback(
    dash.dependencies.Output("CO2-Overall", "figure"),
    [dash.dependencies.Input("country-drop", "value")]
)
def update_figure2(selected_country):
    filtered_df2 = df[df.IndicatorCode.isin(["EN.ATM.CO2E.KT"])]
    filtered_df2_byCountry = filtered_df2[filtered_df2.ShortName == selected_country]
    traces2 = []
    traces2.append(go.Bar(
        x = filtered_df2_byCountry["Year"].tolist(),
        y = filtered_df2_byCountry["Value"].tolist(),
        text = str(filtered_df2_byCountry["IndicatorName"].unique()),
        name = str(filtered_df2_byCountry["IndicatorName"].unique())
    ))
    return {
        "data": traces2,
        "layout": go.Layout(
            xaxis={"type": "linear", "title": "Year"},
            yaxis={"title": "CO2 Emissions"},
            margin={"l": 40, "b": 40, "t": 10, "r": 10},
            hovermode="closest",
            )
    }

print("launch in" + "--- %s seconds ---" % (time.time() - start_time))
if __name__ == "__main__":
    app.run_server()
