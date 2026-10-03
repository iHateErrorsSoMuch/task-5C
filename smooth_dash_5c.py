import time
import threading
from collections import deque

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Adds the newest accelerometer values to the existing graph
def smooth_update(sample, max_points=150):
    timestamp = sample["timestamp"]

    update = {
        "x": [[timestamp], [timestamp], [timestamp]],
        "y": [[sample["X"]], [sample["Y"]], [sample["Z"]]]
    }

    # Update the three traces and keep only the latest points
    return update, [0, 1, 2], max_points

# Handles the accelerometer data and sends it to the graph
class AccelerometerStream:

    def __init__(self, filename):
        self.data = pd.read_csv(filename)
        self.index = 0
        self.buffer = deque(maxlen=500)

    def start(self):
        # Run the data reading in the background
        thread = threading.Thread(target=self.read_data, daemon=True)
        thread.start()

    def read_data(self):
        while True:
            # Get the next row from the Week 8 data
            row = self.data.iloc[self.index]

            sample = {
                "timestamp": row["timestamp"],
                "X": float(row["X"]),
                "Y": float(row["Y"]),
                "Z": float(row["Z"])
            }

            # Store the new sample in the buffer
            self.buffer.append(sample)

            self.index += 1

            # Start again when the end of the file is reached
            if self.index >= len(self.data):
                self.index = 0

            # Controls how quickly new samples are added
            time.sleep(0.15)

    def get_data(self):
        # Return the next sample from the buffer
        if len(self.buffer) > 0:
            return self.buffer.popleft()

        return None

# Start the accelerometer data stream
stream = AccelerometerStream("accelerometer_combined.csv")
stream.start()

app = Dash(__name__)

# Create the three empty graph traces
fig = go.Figure()

fig.add_trace(go.Scatter(x=[], y=[], mode="lines", name="X"))
fig.add_trace(go.Scatter(x=[], y=[], mode="lines", name="Y"))
fig.add_trace(go.Scatter(x=[], y=[], mode="lines", name="Z"))

fig.update_layout(
    title="Live Smartphone Accelerometer",
    xaxis_title="Sample timestamp",
    yaxis_title="Acceleration"
)

# Create the Dash page
app.layout = html.Div([
    html.H2("SIT225 5C - Smooth Live Accelerometer"),

    html.P("Week 8 accelerometer data being updated continuously."),

    dcc.Graph(
        id="accelerometer-graph",
        figure=fig
    ),

    # Calls the update function every 150 milliseconds
    dcc.Interval(
        id="timer",
        interval=150,
        n_intervals=0
    )
])

# Updates the graph when a new sample is available
@app.callback(
    Output("accelerometer-graph", "extendData"),
    Input("timer", "n_intervals")
)
def update_graph(_):

    sample = stream.get_data()

    if sample is None:
        # Do nothing if there is no new data
        return {"x": [[], [], []], "y": [[], [], []]}, [0, 1, 2], 150

    # Use the wrapper to add the new values to the graph
    return smooth_update(sample)


if __name__ == "__main__":
    app.run(debug=False)