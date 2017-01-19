# myapp.py
# Fully inspired / copy from burtn.py in bokeh documentation.

from random import random
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc

import pandas as pd
import numpy as np

# Initialize DF containing the results.
df_electeurs = pd.read_csv("electeurs.csv", sep=";", names=["state", "voters"], skiprows=1)
df_results = df_electeurs.copy()
df_results["party"] = "none"
df_results["Clinton"] = 0
df_results["Trump"] = 0
df_results["Other"] = 0
df_results["added"] = 0
# This is an help to draw chart proportional to voters.
df_results["weight"] = df_results["voters"] / (df_results["voters"].sum())

# Basic Angle for draw
big_angle = 2.0 * np.pi / (len(df_results) + 1)

MAX_VOTERS = 20000000

# For test only
i = 0

def update_results():
    '''
    This will update the df_results df.
    '''
    global df_results
    global i

    if df_results.loc[i*2, "party"] == "none":
        df_results.loc[i*2, "party"] = "republican"
        df_results.loc[i*2, "added"] = len(df_results) - i
        df_results.loc[i*2, "Clinton"] = i * 450000 + 120000
        df_results.loc[i*2, "Trump"] = i * 400000 + 110000
        df_results.loc[i*2, "Other"] = i * 50000 + 11000
    if df_results.loc[i*2 + 1, "party"] == "none":
        df_results.loc[i*2 + 1, "party"] = "democrat"
        df_results.loc[i*2 + 1, "added"] = - len(df_results) + i
        df_results.loc[i*2+1, "Clinton"] = i * 400000 + 110000
        df_results.loc[i*2+1, "Trump"] = i * 500000 + 120000
        df_results.loc[i*2+1, "Other"] = i * 50000 + 11000

    # Sort the DF to democrats, non then republican
    df_results = df_results.sort_values(["party","added"], ascending=[True, True])
    # Reindex the df to make it effective
    df_results.index = range(len(df_results))

    if i < 25:
        i +=1
    else:
        i=0

    return 0

# Here we go in the layer part.

# Just an index to map "party" with a color.
party_color2 = {
    "democrat" : ["#E69483", "#CD8375"],
    "republican" : ["#A7C0F7","#97AEDF"],
    "none" :["#D3D3D3","#C8C8C8" ]
}

candidate_color = {
    "Trump" :   "#c64737",
    "Clinton" : "#0d3362",
    "Other" :  "black",
}

# Figure size
width = 800
height = 800

# Our disc inner and outer radius
inner_radius = 90
outer_radius = 360

# Main figure, a lot of parameters
p = figure(plot_width=width, plot_height=height, title="",
    x_axis_type=None, y_axis_type=None,
    x_range=(-420, 420), y_range=(-420, 420),
    min_border=0, outline_line_color="white",
    background_fill_color="#f0e1d2", border_fill_color="#f0e1d2",
    toolbar_sticky=False)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.logo = None
p.toolbar_location = None


# Annular wedges, with 1 color per party.
wedge = p.annular_wedge(x=0, y=0,
                          inner_radius=inner_radius, outer_radius=outer_radius,
                          start_angle=[], end_angle=[], fill_color=[],
                          color="white").data_source

# The name of the state
state = p.text(x=[], y=[], text=[], angle=[],
             text_font_size="7pt", text_align="center",
             text_baseline="middle").data_source

# # small wedges
wedge_trump = p.annular_wedge(0, 0, inner_radius, outer_radius=[],
                           start_angle=[], end_angle=[],
                           color=candidate_color['Trump'],
                           fill_alpha=0.5).data_source


wedge_clinton = p.annular_wedge(0, 0, inner_radius, outer_radius=[],
                           start_angle=[], end_angle=[],
                           color=candidate_color['Clinton'],
                           fill_alpha=0.5).data_source


wedge_other = p.annular_wedge(0, 0, inner_radius, outer_radius=[],
                           start_angle=[], end_angle=[],
                           color=candidate_color['Other'],
                           fill_alpha=0.5).data_source


#                 -big_angle+angles+5*small_angle, -big_angle+angles+6*small_angle,
#                 color=candidate_color['Penicillin'])
# p.annular_wedge(0, 0, inner_radius, rad(df.streptomycin),
#                 -big_angle+angles+3*small_angle, -big_angle+angles+4*small_angle,
#                 color=candidate_color['Streptomycin'])
# p.annular_wedge(0, 0, inner_radius, rad(df.neomycin),
#                 -big_angle+angles+1*small_angle, -big_angle+angles+2*small_angle,
#                 color=candidate_color['Neomycin'])

# create a callback that will add a number in a random location
def callback():

    # Read the database and update accordingly df_results
    update_results()

    # Update the camemberts
    angle_1 = big_angle / 2 + np.pi / 2
    for line in range(len(df_results)):
        angle = df_results.loc[line, "weight"] * big_angle * len(df_results)
        df_results.loc[line, "angle_0"] = angle_1
        angle_1 = angle_1 + angle
        df_results.loc[line, "angle_1"] = angle_1

    # Color index must reflect the party
    # colors_ = [party_color2[party_code][idx%2] for idx, party_code in enumerate(df_results.party)]
    colors_ = [party_color2[party_code][0] for idx, party_code in enumerate(df_results.party)]

    # Label update
    delta = df_results["angle_0"] + (df_results["angle_1"] - df_results["angle_0"]) / 2
    xr = outer_radius * np.cos(np.array(delta))
    yr = outer_radius * np.sin(np.array(delta))
    label_angle=np.array(delta)
    label_angle[label_angle > (np.pi / 2)] -= np.pi # easier to read labels on the left side
    label_angle[label_angle > (np.pi / 2)] -= np.pi # easier to read labels on the left side

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['start_angle'] = np.array(df_results["angle_0"])
    new_data['end_angle'] = np.array(df_results["angle_1"])
    new_data['fill_color'] = np.array(colors_)
    wedge.data = new_data

    new_data = dict()
    new_data['x'] = xr
    new_data['y'] = yr
    new_data['angle'] = label_angle
    new_data['text'] = df_results.state
    # df_results.state
    state.data = new_data

    new_data = dict()
    delta = (df_results["angle_1"] - df_results["angle_0"]) / 2
    new_data['outer_radius'] = outer_radius * df_results["Trump"] / MAX_VOTERS + inner_radius
    new_data['start_angle'] = np.array(df_results["angle_0"]) + delta + 0.01
    new_data['end_angle'] = np.array(df_results["angle_0"]) + delta + 0.02
    # df_results.state
    wedge_trump.data = new_data

    new_data = dict()
    new_data['outer_radius'] = outer_radius * df_results["Clinton"] / MAX_VOTERS + inner_radius
    new_data['start_angle'] = np.array(df_results["angle_0"]) + delta - 0.01
    new_data['end_angle'] = np.array(df_results["angle_0"]) + delta
    # df_results.state
    wedge_clinton.data = new_data

    new_data = dict()
    new_data['outer_radius'] = outer_radius * df_results["Other"] / MAX_VOTERS + inner_radius
    new_data['start_angle'] = np.array(df_results["angle_0"]) + delta - 0.02
    new_data['end_angle'] = np.array(df_results["angle_0"]) + delta - 0.01
    # df_results.state
    wedge_other.data = new_data

# add a button widget and configure with the call back
button = Button(label="Refresh")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
