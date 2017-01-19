from flask import Flask
from bokeh.sampledata.us_states import data as us_states2
from bokeh.models import (ColumnDataSource, HoverTool, LogColorMapper)
# from bokeh.palettes import RdBu4 as palette
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row
from bokeh.embed import components
from flask import render_template
from bokeh.charts import Histogram
from bokeh.charts import Bar

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Instantiation de notre application
app = Flask(__name__)


# Vue
@app.route('/')
def gui():
    # Loading  of the geometric data of the United States
    us_states = us_states2.copy()

    # Not considering Hawaii et Alaska states (for visualization reasons)
    del us_states["HI"]
    del us_states["AK"]

    # Longitudes et latitudes associées à chaque état
    state_xs = [us_states[code]["lons"] for code in us_states]
    state_ys = [us_states[code]["lats"] for code in us_states]

    # Nom de chaque état
    state_names = [us_states[code]["name"] for code in us_states]

    # Generating (randomly) the outcome of the election

    # Considering 49 states out of 51 (Hawaii and Alaska excluded for now)
    # Considering 2 candidates (Hillary, Trump)
    result_hillary = np.random.uniform(0, 100, 49)
    result_trump = (100 - result_hillary)
    result_election = np.array([result_hillary, result_trump]).T



    idx_state_winner = np.zeros(result_election.shape[0])
    for i in range(result_election.shape[0]):
        if result_election[i, 0] > result_election[i, 1]:
            idx_state_winner[i] = 0
        else:
            idx_state_winner[i] = 1

    # idx_state_winner = interpret_result(result_election)

    nb_states_hillary = np.sum(idx_state_winner == 0)
    nb_states_trump = np.sum(idx_state_winner == 1)

    result_hillary = result_hillary.tolist()
    result_trump = result_trump.tolist()

    idx_state_winner = idx_state_winner.tolist()

    source = ColumnDataSource(data=dict(x=state_xs,
                                        y=state_ys,
                                        name=state_names,
                                        idx_state_winner=idx_state_winner,
                                        result_hillary=result_hillary,
                                        result_trump=result_trump
                                        ))

    # Red and blue color (only)
    # palette = [palette[-1], palette[0]]

    # Couleurs que chaque état pourra avoir (dépendant du résultat de l'état)
    colors = ["#FF0000", "#0000FF"]
    color_mapper = LogColorMapper(palette=colors)

    tools = "pan,wheel_zoom,box_zoom,reset,hover,save"

    # Panel 1: Interactive Map
    p1 = figure(title="2016 USA Presidential Election", x_axis_location=None, y_axis_location=None,
               tools=tools, toolbar_location="left", plot_width=800, plot_height=600)  #  plot_width=1100, plot_height=700

    p1.patches('x', 'y', source=source,
              fill_color={'field': 'idx_state_winner', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)

    p1.grid.grid_line_color = None

    hover = p1.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [("Name", "@name"), ("(Long, Lat)", "($x, $y)"),
                      ("(Hillary, Trump)", "(@result_hillary%, @result_trump%)")]

    # Panel 2: Some interactive statistics (e.g.: histogram plots)
    p2 = figure(title="Number of states won by each candidate", width=400, height=600)
    p2.vbar(x=[1, 2], top=[nb_states_hillary, nb_states_trump], width=0.5, bottom=0, color=colors)

    script, div = components(row(p1, p2))

    # Template (HTML) à retourner
    return render_template('dashboard.html', script=script, div=div)

if __name__ == '__main__':
    app.run(debug=True)
