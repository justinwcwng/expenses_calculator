# This dash app creates an easy-to-use shopping expenses calculator
#
# Created and maintained by Justin Wong - justinwcwng@gmail.com
#
# Kindly visit http://127.0.0.1:8050/ in your web browser

from dash import Dash, html, Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
server = app.server
app.title = "Justin's Calculator"

ppl = ["Callum", "Justin"]
currency = "£"

app.layout = dbc.Container([
    # heading row - description at the top
    dbc.Row([
        html.H1(children="Calculate Your Expenses"),
        html.Br(),
        dbc.Button("Add Item",
                   color="primary",
                   id="add-item-btn",
                   n_clicks=0,
                   style={
                       "width": "25vw",
                       "border-radius": "1rem",
                       "justify-content": "center"
                   }),
        html.Br()
    ]),
    # content row with left and right sections
    dbc.Row([
        # left section (scrollable)
        dbc.Col([
            html.Br(),
            html.Div(id="items-container",
                     style={
                         "height": "80vh",
                         "overflowY": "auto", # enable vertical scrolling
                         "padding-right": "15px" # padding for the scrollbar
                     })
            ]),
        # right section (scrollable)
        dbc.Col([
            html.Br(),
            html.Div(id="msg-container",
                     style={
                         "height": "80vh",
                         "overflowY": "auto",
                         "padding-right": "15px"
                     })
            ])
    ])
], fluid=True)

@callback(
    Output("items-container", "children"),
    Input("add-item-btn", "n_clicks"),
    State("items-container", "children")
)
def update_items_container(n, existing_children):
    if n is None:
        return []
    
    if existing_children is None:
        existing_children = []

    new_item = dbc.Form(children=[

        dbc.Row([
            dbc.Col([
                dbc.Label(f"Item {n+1} ")
                ],
            xs=4,
            sm=4,
            md=4,
            lg=2
            ),
            dbc.Col([
                dbc.Input(
                    id={"type": "item-name-input", "index": n},
                    value="",
                    type="text"
                )
            ]),
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Label("VAT"),
                xs=4,
                sm=4,
                md=4,
                lg=2
            ),
            dbc.Col(
                dbc.RadioItems(
                    id={"type": "vat-input", "index": n},
                    options=[
                        {"label": "A (Yes)", "value": True},
                        {"label": "Z (No)", "value": False}
                    ],
                    value=False,
                    inline=True
                )
            )
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Label("Share"),
                xs=4,
                sm=4,
                md=4,
                lg=2
            ),
            dbc.Col(
                dbc.Checklist(
                    id={"type": "share-input", "index": n},
                    options=ppl,
                    value=ppl,
                    inline=True
                ),
            )
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Label(f"{currency} "),
                xs=4,
                sm=4,
                md=4,
                lg=2
            ),
            dbc.Col(
                dbc.Input(
                    id={"type": "price-input", "index": n},
                    value=0,
                    type="number"
                )
            )
        ]),

    ], style={
        "color": "white",
        "backgroundColor": "#222222",
        "opacity": 0.7,
        "padding": "2rem",
        "border-radius": "2rem"
    })

    return existing_children + [new_item, html.Br()]

@callback(
    Output("msg-container", "children"),
    Input({"type": "item-name-input", "index": ALL}, "value"),
    Input({"type": "vat-input", "index": ALL}, "value"),
    Input({"type": "share-input", "index": ALL}, "value"),
    Input({"type": "price-input", "index": ALL}, "value")
)
def update_msg_container(name_inputs, vat_inputs, share_inputs, price_inputs):
    if not price_inputs: # if no items have been added yet
        return html.Div("No items added yet.")

    n = len(price_inputs)
    priceVAT = price_inputs.copy()

    # apply VAT
    for i, (price, vat) in enumerate(zip(price_inputs, vat_inputs)):
        if price is None: priceVAT[i] = 0
        if vat: priceVAT[i] = 1.2 * price
    
    total = sum(priceVAT)
    average = total / n if n > 0 else 0

    counts = [len(person_names) for person_names in share_inputs]
    ppp = [price / count for price, count in zip(priceVAT, counts) if count > 0]

    share_list = {person: 0 for person in ppl}
    for i, (price, shared_with) in enumerate(zip(ppp, share_inputs)):
        for person in shared_with:
            share_list[person] += price

    msg = html.Div([
        html.H2(children="Your Purchase Summary"),
        html.H3(children=f"You purchased {n} items."),
        html.H3(children=f"Total amount spent is {currency} {total:.2f}."),
        html.H3(children=f"Average item price is {currency} {average:.2f}."),
        html.Br(),
        html.Div([
            html.Div([html.Div(f"Item {i+1}: {item_name}") for i, item_name in enumerate(name_inputs)]),
            html.Div([html.Div(f"{currency} {price:.2f}") for price in priceVAT])
            ], style={
                "display": "flex",
                "justify-content": "space-between"
                }),
        html.Br(),
        html.Div([html.H3([f"{person_name} pays {currency} {share:.2f}", html.Br()]) for person_name, share in share_list.items()])
        ])
    return msg

if __name__ == "__main__":
    app.run(debug=True)
