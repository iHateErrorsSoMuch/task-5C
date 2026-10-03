SIT225 5C - Smooth Plotly Dash Accelerometer

1. Put this file in the same folder as:
   accelerometer_combined.csv

2. Install packages:
   pip install -r requirements.txt

3. Run:
   python smooth_dash_5c.py

4. Open the local Dash address shown in the terminal.

The application replays the Week 8 smartphone accelerometer data as a
continuous stream. The graph uses Plotly's extendData mechanism so new
samples are appended to existing traces rather than rebuilding the entire
figure.

The reusable smooth_update() wrapper exposes the core update mechanism.
