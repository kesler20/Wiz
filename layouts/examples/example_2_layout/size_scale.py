from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Size scale layout
##==================================
def get(min_size, max_size):
    scale = html.Iframe(srcDoc = '''
        <div id="size-scale-inner", width = 100%>
            <svg width="100%" height="30px">
              <g id="size-scale-graphics">
                  <svg height = "100%", width = "100%", viewBox = "0 0 100 100", preserveAspectRatio = "none">
                    <polygon id="traingle" points="5,50 95,75 95,25" stroke="#cccccc" stroke-width="1" fill-opacity="1.0" fill="#000" />
                  </svg>
                  <circle id="min-circle" cx="5%" cy="50%" r="5" stroke="#cccccc" stroke-width="1" fill-opacity="1.0" fill="#000" />
                  <circle id="max-circle" cx="95%" cy="50%" r="15" stroke="#cccccc" stroke-width="1" fill-opacity="1.0" fill="#000" />
              </g>
            </svg>
        </div>
        ''',
        style = dict(
           height = 50,
           width = '100%',
           borderStyle = 'none',
           zIndex = 5,
        ),
    )

    out = html.Div(
        dbc.Row(
            [
                html.H6(min_size,id = 'example-2-min-size', style= dict(display = 'inline-block')),
                html.Div(scale, id = 'example-2-size-scale', style= dict(display = 'inline-block', width = '50%')),
                html.H6(max_size,id = 'example-2-max-size', style= dict(display = 'inline-block')),
            ],
        align = 'center',
        justify = 'center'
        ),
        id = 'example-2-display-size-scale',
        style = dict(display = 'block')
    )

    return out
