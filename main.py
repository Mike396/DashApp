from dash import html, dcc, Output, Input, State, MATCH, ALL, ALLSMALLER, ctx
import dash
import dash_bootstrap_components as dbc

my_dict = {
    "DK": ["Aarhus", "Odense", "Copenhagen"],
    "UK": ["Birmingham", "Liverpool", "Manchester"],
    "ESP": ["Madrid", "Barcelona", "Sevilla"]
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(dbc.Button(children="Add", id="add-button", n_clicks=0)),
    html.Div(children=[], id="container")
])


@app.callback(
    Output("container", "children"),
    Input("add-button", "n_clicks"),
    Input({"type": "delete-button", "index": ALL}, "n_clicks"),
    State("container", "children")
)
def func1(n_clicks, del_btn, div_children):
    trig = ctx.triggered_id

    if trig == "add-button":
        new_child = html.Div(
            style={'display': 'inline-block', 'outline': 'thin black solid', "padding": "5px", "margin": "2px"},
            children=[
                html.Div(dcc.RadioItems(id={"type": "country", "index": n_clicks}, options=list(my_dict.keys()), value="DK")),
                html.Br(),
                html.Div(dcc.RadioItems(id={"type": "cities", "index": n_clicks})),
                html.Br(),
                html.Div(id={"type": "text-output", "index": n_clicks}),
                html.Br(),
                html.Div(dbc.Button(children="Delete", id={"type": "delete-button", "index": n_clicks}), n_clicks=0)
            ])

        div_children.append(new_child)
        return div_children

    elif trig["type"] == "delete-button":
        div_new = []
        for i in range(len(div_children)):
            if div_children[i]["props"]["children"][0]["props"]["children"]["props"]["id"]["index"] != trig["index"]:
                div_new.append(div_children[i])
        return div_new


@app.callback(
    Output({"type": "cities", "index": MATCH}, "options"),
    Input({"type": "country", "index": MATCH}, "value"),
)
def func2(country):
    return my_dict[country]


@app.callback(
    Output({"type": "text-output", "index": MATCH}, "children"),
    Input({"type": "country", "index": MATCH}, "value"),
    Input({"type": "cities", "index": MATCH}, "value"),
)
def func3(country, city):
    txt_output = f"You chose {country} with the city {city}"
    return txt_output


if __name__ == '__main__':
    app.run()
