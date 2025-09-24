from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from app import app


##==================================
## Card content
##==================================
example_1_content = [
    dbc.CardBody(
        [
            html.H5("Live Data Plotting", className="card-title"),
            html.H6(
                [
                    "Future applications of Wiz will allow you to visualize and analyze your "
                    "data as it is generated. Check out this example that updates "
                    "the plot as new data comes in."
                ]
            ),
            dbc.CardLink(html.Img(src=app.get_asset_url('images/Example_1.gif'), className = 'example-gif'), href="/example-1")
        ]
    ),
]

example_2_content = [
    dbc.CardBody(
        [
            html.H5("High-throughput Screening for Materials Discovery", className="card-title"),
            html.H6(
                [
                    "Recently, we used high-throughput screenings to identify top materials for "
                    "oxygen storage. The dataset consists of nearly ~20 "
                    "descriptors with nearly 3000 instances. Read the ",

                    html.A('original paper ',
                        href = 'https://www.nature.com/articles/s41467-018-03892-8',
                        target="_blank",
                        style = dict(color = 'white', textDecoration = 'underline')
                    ),

                    "for more info. "
                ]
            ),

            dbc.CardLink(html.Img(src=app.get_asset_url('images/Example_2.gif'), className = 'example-gif'), href="/example-2")
        ]
    ),
]


example_3_content = [
    dbc.CardBody(
        [
            html.H5("Line Plots - Stock Data", className="card-title"),
            html.H6(
                [
                    "Plot line series in Wiz with ease. This example "
                    "allows you to plot stock market data in the Wiz environment. "
                    "Download the data to see how it is formatted!"
                ]
            ),
            dbc.CardLink(html.Img(src=app.get_asset_url('images/Example_3.gif'), className = 'example-gif'), href="/example-3")
        ]
    ),
]

example_4_content = [
    dbc.CardBody(
        [
            html.H5("Box Plots - Wine Classification", className="card-title"),
            html.H6(
                [
                    "Within the scatter function of Wiz, if your x-axis has "
                    "categorical data, box plots will automatically be produced. "
                    "Try it out with this example of a popular wine classification "
                    "dataset! Dataset obtained from ",


                    html.A('UCI Repository.',
                        href = 'https://archive.ics.uci.edu/ml/datasets/Wine',
                        target="_blank",
                        style = dict(color = 'black', textDecoration = 'underline')
                    ),
                ]
            ),

            dbc.CardLink(html.Img(src=app.get_asset_url('images/Example_4.gif'), className = 'example-gif'), href="/example-4")
        ]
    ),
]

example_5_content = [
    dbc.CardBody(
        [
            html.H5("Principle Component Analysis - Iris Data", className="card-title"),
            html.H6(
                [
                    "If you need to do basic analysis on your dataset, use the "
                    "Principle Component Analysis tool! You upload your dataset and Wiz "
                    "will automatically perform two-component PCA (or LDA) on your dataset. "
                    "This example shows the output for the popular Iris dataset. Dataset obtained from ",


                    html.A('UCI Repository.',
                        href = 'https://archive.ics.uci.edu/ml/datasets/Iris',
                        target="_blank",
                        style = dict(color = 'white', textDecoration = 'underline')
                    ),
                ]
            ),

            dbc.CardLink(html.Img(src=app.get_asset_url('images/Example_5.gif'), className = 'example-gif'), href="/example-5")
        ]
    ),
]


##==================================
## Assemble cards
##==================================
cards = dbc.CardColumns(
    [
        dbc.Card(example_1_content, color = 'light'),
        dbc.Card(example_2_content, color = 'secondary', inverse = True),
        dbc.Card(example_3_content, color = 'primary', inverse = True),
        dbc.Card(example_4_content, color = 'light'),
        dbc.Card(example_5_content, color = 'secondary',inverse = True),

    ]
)

def get():
    return cards
