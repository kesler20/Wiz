import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Bubble logo
##==================================
bubble_logo = html.Div([
    html.Iframe(srcDoc = '''
        <body style="margin: 0px">
            <script type="text/javascript" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
            <script type="text/javascript" src="https://s3.amazonaws.com/codecademy-content/courses/hour-of-code/js/alphabet.js"></script>
            <canvas id="myCanvas" height="100%" width="100%"></canvas>
            <script type="text/javascript" src="https://codepen.io/cbalzer/pen/zmebNz.js"></script>
            <script type="text/javascript" src="https://codepen.io/cbalzer/pen/JVzzjG.js"></script>
        </body>
    ''',
    style = dict(
        borderStyle = 'none',
        position = 'absolute',
        height = 110,
        left = '-3%',
        top = '0.5%',
        overflow = 'visible',
        zIndex = 1000,
        margin = 0,
        verticalAlign = 'middle'
    ))
])

def get():
    return bubble_logo
