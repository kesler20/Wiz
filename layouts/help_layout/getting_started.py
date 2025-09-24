from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from app import app
##==================================
## What is Wiz?
##==================================
what_is_wiz = dbc.Container(
    [
        html.H3("What is Wiz?"),
        html.P([
            "Wiz is a convienient tool for interactively plotting "
            "data. Wiz allows users to "
            "quickly explore their data with fast switching between "
            "plot types and data series. Built-in features allow "
            "users to filter their data, edit plot layouts, and "
            "even print high quality images of their graphs. Check out "
            "our ",
            html.A("original publication",
                href = 'https://doi.org/10.1016/j.patter.2020.100107',
                target="_blank"
            ),
            ", the help guide, the video, and the info below to get started!"
            ],
            className="lead",
        ),
        html.Br(),
        html.Video(src=app.get_asset_url('videos/Wiz_Demo.mp4'), controls = True, preload = 'auto', className = 'displayVid')
    ],
    fluid=True,
)
##==================================
## Usage
##==================================
card_1 = [
    dbc.CardBody(
        [
            html.H5("1. Request a password"),
            html.P(
                [
                    "We require a password for use so we can understand the extent of usership. "
                    "If you need a password, then ",
                    dcc.Link("request one ",
                        href = '/request-password',
                        style = dict(color = 'white', textDecoration = 'underline')
                    ),
                    "and it will be emailed to you. "
                    "Once you have the password, simply enter it on the homepage to access Wiz.",
                ],
                className="card-text",
            ),
        ]
    ),
]

card_2 = [
    dbc.CardBody(
        [
            html.H5("2. Upload your data"),
            html.P(
                [
                    "Wiz plots your dataset, but you'll need to upload your data "
                    "in correct format (see ",
                    dcc.Link("Examples",
                        href = '/examples',
                        style = dict(color = 'white', textDecoration = 'underline')
                    ),
                    "). Wiz caches your data for use "
                    "during your session. Data is deleted from our server after you "
                    "are finished plotting.",
                ],
                className="card-text",
            ),
        ]
    ),
]

card_3 = [
    dbc.CardBody(
        [
            html.H5("3. Explore your dataset"),
            html.P("Now that your data is uploaded, you can interactively explore your data! "
                "See the examples and the original documentation to see all of the ways you can use Wiz!",
                className="card-text",
            ),
        ]
    ),
]

##==================================
## Getting started
##==================================
get_started = dbc.Container(
        [
            html.H3("Getting started..."),
            html.Br(),
            html.H4(html.A('Wiz Help Guide',target = '_blank',href='assets/docs/Wiz_Help.pdf')),
            html.Br(),
            dbc.CardDeck(
                [
                    dbc.Card(card_1, color="primary", inverse=True),
                    dbc.Card(card_2, color="secondary", inverse=True),
                    dbc.Card(card_3, color="dark", inverse=True)
                ]
            ),
            html.P("Each page of the application has more specific usage information, particularly for data upload formats."),
        ],
        fluid=True,
)

##==================================
## FAQs
##==================================
FAQs = dbc.Container(
        [
            html.H3("FAQs"),
            html.P(
                [
                    html.H5('1. How do I cite Wiz?'),
                    html.P(
                        [
                            "To cite Wiz, simply reference the ",
                            html.A("original publication.",
                                href = 'https://doi.org/10.1016/j.patter.2020.100107',
                                target="_blank"
                            ),
                        ]
                    ),

                    html.H5('2. What kinds of plots can I make?'),
                    html.P("Currently, you can make histograms, box plots, 2D/3D scatter "
                    "plots, and line series. If your data is appropriate, you "
                    "can also do Principle Component Analysis or Linear Discriminant "
                    "Analysis."
                    ),

                    html.H5('3. Where does my data go?'),
                    html.P("When you upload your dataset, we temporarily store the "
                    "dataset on our server via caching. The files expire 30 minutes after "
                    "upload. If you have concerns about data security, please reach out to us."
                    ),

                    html.H5('4. How is Wiz built?'),
                    html.P("Wiz is built using Plotly's Dash framework. That means "
                    "that all of the components, graphing, and analysis is done in "
                    "pure Python. Dash has an extensive and active community if you "
                    "are interested in building something like Wiz."
                    )
                ]
            )
        ],
        fluid=True,
)


##==================================
## Assemble Jumbotron
##==================================
out = dbc.Jumbotron(
    [
        what_is_wiz,
        html.Br(),
        get_started,
        html.Br(),
        FAQs
    ]
)



def get():
    return out
