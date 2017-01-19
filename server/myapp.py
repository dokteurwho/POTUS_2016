# myapp.py
# Fully inspired / copy from burtn.py in bokeh documentation.

from random import random
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
import pandas as pd
import numpy as np
import pymongo

# Constants are here.
PATH_VOTERS = "electeurs.csv"

# MAX_VOTERS must contain the maximum of citizen voting for 1 candidate
# Calfifornia, 8 753 788 for Clinton.
MAX_VOTERS = 10000000
REMOTE_DB_IP = "35.156.198.242"
MONGO_CLI = "mongodb://{}:27017".format(REMOTE_DB_IP)

# Initialize df_caneva storing state names, state ID and number of voters.
df_electeurs = pd.read_csv(PATH_VOTERS, sep=";",
                           names=["state", "voters", "state_id"], skiprows=1,
                           encoding="utf-8")
df_caneva = df_electeurs.copy()
# Set everything to 0.
df_caneva["party"] = "none"
df_caneva["added"] = 0
# This is an helper to draw chart proportional to voters.
df_caneva["weight"] = df_caneva["voters"] / (df_caneva["voters"].sum())

#  Angle for draw the chart
big_angle = 2.0 * np.pi / (len(df_caneva) + 1)

print("Connecting to {}".format(MONGO_CLI))
mongo_client = pymongo.MongoClient(MONGO_CLI)
print("Data base are:")
print(mongo_client.database_names())

def update_results():
    '''
    This will update the df_results df.
    '''
    global df_results

    # Get DB content.
    print("Refresh ...")
    db_content = mongo_client.POTUS.synthese.find()

    # Create a DF with DB content
    dic_election_list =[]
    for col in db_content:
        row = [col['state'], col['Trump'], col['Clinton'], col['Other']]
        dic_election_list.append(row)
    df_db = pd.DataFrame(dic_election_list,
                         columns=["state_id", "Trump", "Clinton", "Other"])

    # Merge with caneva DF
    df_results = pd.merge(df_caneva, df_db, how='left', on=["state_id"]).fillna(0)

    # Set the wining party
    for i in range(len(df_results)):

        if df_results.loc[i, "Trump"] > df_results.loc[i, "Clinton"]:
            df_results.loc[i, "party"] = "republican"
            # This is just a way to sort in a proper way the result
            df_results.loc[i, "added"] =  - len(df_results) + i
        elif df_results.loc[i, "Trump"] < df_results.loc[i, "Clinton"]:
            df_results.loc[i, "party"] = "democrat"
            # This is just a way to sort in a proper way the result
            df_results.loc[i, "added"] = len(df_results) - i
    #print(df_results)

    # Sort the DF to democrats, non then republican
    df_results = df_results.sort_values(["party", "added"], ascending=[True, True])
    # Reindex the df to make it effective
    df_results.index = range(len(df_results))

# Here we go in the layer part.

# Just an index to map "party" with a color.
party_color2 = {
    "democrat" : ["#E69483", "#CD8375"],
    "republican" : ["#A7C0F7","#97AEDF"],
    "none" :["#D3D3D3","#C8C8C8" ]
}

candidate_color = {
    "Clinton" :   "#C64737",
    "Trump" : "#0D3362",
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

# circular axes and lables
labels = np.arange(0, MAX_VOTERS, MAX_VOTERS//4)
radii = outer_radius * labels / MAX_VOTERS + inner_radius

circular_axes = p.circle(0, 0, radius=radii,
                         fill_color=None, line_color="white").data_source

p.text(0, radii[:-1], [str(r) for r in labels[:-1]],
       text_font_size="8pt", text_align="center", text_baseline="middle")

# The name of the state
state = p.text(x=[], y=[], text=[], angle=[],
             text_font_size="7pt", text_align="center",
             text_baseline="middle").data_source

# # The name of the state
# results_display = p.text(x=0, y=0, text="Hello",
#              text_font_size="14pt", text_align="center",
#              text_baseline="middle").data_source

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

    # Jusr redraw axes
    circular_axes.data = None

    # Winner projection
    tmp_results = df_results.groupby("party")["voters"].sum()

    if "none" not in df_results["party"]:
        str_res = "Final result: "
    else:
        str_res = "Projection: "

    if "democrat" in tmp_results and "republican" in tmp_results:
        if tmp_results["democrat"] >  tmp_results["republican"]:
            str_res += "Clinton."
        else:
            str_res += "Trump."
    else:
        str_res = "Result"

    new_data = dict()
    new_data['text'] = [str_res]
    results_display.data = new_data

# add a button widget and configure with the call back
button = Button(label="Refresh")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
