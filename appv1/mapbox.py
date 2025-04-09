import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Load your data
for i in range(0, 40):  # Loop from 1 to 40
    # Construct the filename
    filename = f'/home/ubuntu/backend/data/full_compiled_data{i}.csv'
    # Load the dataset into a DataFrame
    df = pd.read_csv(filename)
    # Create a dynamic variable name like df1, df2, ..., df40
    a = 1981 + i
    globals()[f'df{a}'] = df

# Callback to update the graph based on user selection
# Callback to update the graph based on user selection
# @app.callback(Output('intermediate-value', 'data'), [Input('btn-wss', 'n_clicks'),
#                Input('btn-wcs', 'n_clicks'),
#                Input('btn-scw', 'n_clicks'),
#                Input('btn-wpd_median', 'n_clicks'),
#                Input('btn-wpd_mean', 'n_clicks'),
#                Input('btn-ghi_median', 'n_clicks'),
#                Input('btn-ghi_mean', 'n_clicks'),
#                Input('btn-wpd_availability', 'n_clicks'),
#                Input('btn-ghi_availability', 'n_clicks'),
#                Input('btn-wind_ep_length', 'n_clicks'),
#                Input('btn-wind_ep_lull', 'n_clicks'),
#                Input('btn-solar_ep_length', 'n_clicks'),
#                Input('btn-solar_ep_lull', 'n_clicks')
#                ])
# def data_store(wss_clicks, wcs_clicks, scw_clicks, wpd_median_clicks, wpd_mean_clicks, ghi_median_clicks, ghi_mean_clicks, wpd_availability_clicks, ghi_availability_clicks,solar_ep_lull_clicks,solar_ep_length_clicks,wind_ep_lull_clicks,wind_ep_length_clicks):
#      # some expensive data processing step   
#     ctx = dash.callback_context
#     if ctx.triggered and 'year-slider' not in ctx.triggered[0]['prop_id']:
#         # If a button was clicked, update the chosen dataset
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#         chosen_datastat = button_id.split('-')[1]
#      # more generally, this line would be
#      # json.dumps(cleaned_df)
#         return chosen_datastat

# Callback to update the graph based on user selection
def update_figure(value,year,in_lat,in_lon,clicks):
    # Determine which button was clicked
    # Get the variable from button ID
    if clicks is None:
        clicks = 0
    if value is None:
        chosen_datastat = 'wss'
    else:
        chosen_datastat = value
    dynamic_df = globals()[f'df{int(year)}']
    # cities = pd.read_csv(f'/Users/bharukashiv/Desktop/BTP/cities.csv')
    color_value_map = {
        'wpd_median': 'color_wpd_median',
        'ghi_median': 'color_ghi_median',
        'wpd_mean': 'color_wpd_mean',
        'ghi_mean': 'color_ghi_mean',
        'wpd_availability': 'color_wpd_availability',
        'ghi_availability': 'color_ghi_availability',
        'wss': 'color_wss',
        'scw': 'color_scw',
        'wcs': 'color_wcs',
        'wind_ep_length': 'color_wind_ep_length',
        'wind_ep_lull': 'color_wind_ep_lull',
        'solar_ep_length': 'color_solar_ep_length',
        'solar_ep_lull': 'color_solar_ep_lull'
    }
    color_bar_title = {
        'wpd_median': 'W/m²',
        'ghi_median': 'W/m²',
        'wpd_mean': 'W/m²',
        'ghi_mean': 'W/m²',
        'wpd_availability': '%',
        'ghi_availability': '%',
        'wss': '%',
        'scw': '%',
        'wcs': '%',
        'wind_ep_length': 'Hours',
        'wind_ep_lull': 'Hours',
        'solar_ep_length': 'Hours',
        'solar_ep_lull': 'Hours'
    }
    title_map = {
    'wpd_median': 'Wind Power Density Median (W/m²)',
    'ghi_median': 'Global Horizontal Irradiance Median (W/m²)',
    'wpd_mean': 'Wind Power Density Mean (W/m²)',
    'ghi_mean': 'Global Horizontal Irradiance Mean (W/m²)',
    'wpd_availability': 'Wind Power Density Availability (%)',
    'ghi_availability': 'Global Horizontal Irradiance Availability (%)',
    'wss': 'Wind Solar Synergy (%)',
    'scw': 'Solar Complements Wind (%)',
    'wcs': 'Wind Complements Solar (%)',
    'wind_ep_length': 'Wind Episode Lengths (Hours)',
    'wind_ep_lull': 'Wind Episode Lulls (Hours)',
    'solar_ep_length': 'Solar Episode Lenghts (Hours)',
    'solar_ep_lull': 'Solar Episode Lulls (Hours)'

    }   

    df_sub = dynamic_df[['latitude', 'longitude', chosen_datastat, color_value_map[chosen_datastat]]]
    text_a =[f"WPD Median: {wpd_median:.2f}<br>"
      f"WPD Mean: {wpd_mean:.2f}<br>"
      f"GHI Median: {ghi_median:.2f}<br>"
      f"GHI Mean: {ghi_mean:.2f}<br>"
      f"Wind Availability: {wpd_availability:.2f}<br>"
      f"Solar Availability: {ghi_availability:.2f}<br>"
      f"Wind Solar Synergy: {wss:.2f}<br>"
      f"Solar Complements Wind: {scw:.2f}<br>"
      f"Wind Complements Solar: {wcs:.2f}<br>"
      f"Wind Episode Lengths: {wind_ep_length:.2f}<br>"
      f"Wind Episode Lulls: {wind_ep_lull:.2f}<br>"
      f"Solar Episode Lenghts: {solar_ep_length:.2f}<br>"
      f"Solar Episode Lulls: {solar_ep_lull:.2f}<br>"
      "<extra></extra>"  # Suppress extra hover information
      for wpd_median, wpd_mean, ghi_median, ghi_mean, wpd_availability, ghi_availability, wss, scw, wcs, wind_ep_length, wind_ep_lull, solar_ep_length, solar_ep_lull 
      in zip(dynamic_df['wpd_median'], dynamic_df['wpd_mean'], dynamic_df['ghi_median'], dynamic_df['ghi_mean'],
             dynamic_df['wpd_availability'], dynamic_df['ghi_availability'], dynamic_df['wss'], dynamic_df['scw'], dynamic_df['wcs'], dynamic_df['wind_ep_length'], dynamic_df['wind_ep_lull'], dynamic_df['solar_ep_length'], dynamic_df['solar_ep_lull'])]
    # Define color scales based on the selected data stat
    color_scale_map = {
        'wpd_median': 'speed',
        'ghi_median': 'magma',
        'wpd_mean': 'speed',
        'ghi_mean': 'magma',
        'wpd_availability': 'RdBu',
        'ghi_availability': 'RdBu',
        'wss': 'Reds',
        'scw': 'solar',
        'wcs': 'Blues',
        'wind_ep_length': 'speed',
        'wind_ep_lull': 'speed',
        'solar_ep_length': 'magma',
        'solar_ep_lull': 'magma_r'

    }



    #------------------------------------------------------Zoom Functionality---------------------------------------------------------------
    if clicks > 0 and in_lat is not None and in_lon is not None:
        z = 7
        c = {'lon' : in_lon, 
             'lat' : in_lat}
    else: 
        z = 5
        c = {'lon': 79, 'lat': 23}
    # def haversine(lat1, lon1, lat2, lon2):
    #     # Convert latitude and longitude from degrees to radians
    #     lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    #     # Haversine formula
    #     dlon = lon2 - lon1 
    #     dlat = lat2 - lat1 
    #     a = np.sin(dlat/2)*2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)*2
    #     c = 2 * np.arcsin(np.sqrt(a)) 
        
    #     # Radius of Earth in kilometers (use 3956 for miles)
    #     r = 6371  
    #     return c * r

    # def find_nearest(lat, lon, locations):
    #     nearest_location = None
    #     min_distance = float('inf')  # Start with an infinitely large distance
        
    #     for loc in locations:
    #         loc_lat, loc_lon = loc
    #         distance = haversine(lat, lon, loc_lat, loc_lon)
            
    #         if distance < min_distance:
    #             min_distance = distance
    #             nearest_location = (loc_lat, loc_lon)
        
    #     return nearest_location
    # if click > 0 and in_lat is not None and in_lon is not None:
    #     nearest_coordinates = find_nearest(in_lat, in_lon, [df_sub['latitude'],df_sub['longitude']])
#=------------------------------------------------------------------------------------------------------------------
    # Create figure
    locations = [go.Scattermapbox(
        lon=df_sub['longitude'],
        lat=df_sub['latitude'],
        mode='markers',
        text = text_a,
        textfont=dict(size=28, color='white'),
        marker={'color': df_sub[color_value_map[chosen_datastat]],
            'size': 10,
            'opacity': 1,
            'colorscale': color_scale_map[chosen_datastat],
            'colorbar': {
                'title': color_bar_title[chosen_datastat],
                'thickness': 30,
                'len': 0.5,
                'x': 0.9,  # Keep it inside the map
                'xanchor': 'left',
                'y': 0.5,
                'yanchor': 'middle',
                'bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent background
                'tickcolor': 'white',  # Set tick color to white
                'titlefont': {'family' : 'Georgia, serif','size': 42,'color': 'black'},  # Set the title color to white
                'tickfont': {'family' : 'Georgia, serif','size' : 42,'color': 'black'}  # Set tick label font color to white
            }
        },
        unselected={'marker': {'opacity': 0.7, 'size': 2}},
        selected={'marker': {'opacity': 0.5, 'size': 25}},
        hovertemplate=
            "<b>WPD Median:</b> %{customdata[0]:.2f} W/m²<br>" +
            "<b>WPD Mean:</b> %{customdata[1]:.2f} W/m²<br>" +
            "<b>GHI Median:</b> %{customdata[2]:.2f} W/m²<br>" +
            "<b>GHI Mean:</b> %{customdata[3]:.2f} W/m²<br>" +
            "<b>Wind Availability:</b> %{customdata[4]:.2f} %<br>" +
            "<b>Solar Availability:</b> %{customdata[5]:.2f} %<br>" +
            "<b>Wind Solar Synergy:</b> %{customdata[6]:.2f} %<br>" +
            "<b>Solar Complements Wind:</b> %{customdata[7]:.2f} %<br>" +
            "<b>Wind Complements Solar:</b> %{customdata[8]:.2f} %<br>" +
            "<b>Wind Episode Lengths:</b> %{customdata[9]:.2f} Hours<br>" +
            "<b>Wind Episode Lulls:</b> %{customdata[10]:.2f} Hours<br>" +
            "<b>Solar Episode Lengths:</b> %{customdata[11]:.2f} Hours<br>" +
            "<b>Solar Episode Lulls:</b> %{customdata[12]:.2f} Hours<br>" +
            "<extra></extra>",

        hoverlabel=dict(
        font=dict(size=32)),
        customdata=np.column_stack((df['wpd_median'], df['wpd_mean'], df['ghi_median'],
                               df['ghi_mean'], df['wpd_availability'], df['ghi_availability'],
                               df['wss'], df['scw'], df['wcs'], df['wind_ep_length'],df['wind_ep_lull'], df['solar_ep_length'], df['solar_ep_lull'])),
        showlegend=False  
    )]

    graphData = [
    {
        "type": "scattermapbox",
        "lat": df_sub['latitude'].tolist(),  # Convert latitude to list
        "lon": df_sub['longitude'].tolist(),  # Convert longitude to list
        "mode": "markers",
        "text": text_a,  # Assuming text_a is pre-defined
        "textfont": {
            "size": 28,
            "color": "white"
        },
        "marker": {
            "color": df_sub[color_value_map[chosen_datastat]].tolist(),
            "size": 10,
            "opacity": 1,
            "colorscale": color_scale_map[chosen_datastat],
            "colorbar": {
                "title": color_bar_title[chosen_datastat],
                "thickness": 30,
                "len": 0.5,
                "x": 0.9,  # Keep it inside the map
                "xanchor": 'left',
                "y": 0.5,
                "yanchor": 'middle',
                "bgcolor": 'rgba(0, 0, 0, 0)',  # Transparent background
                "tickcolor": 'white',  # Set tick color to white
                "titlefont": {
                    'family': 'Georgia, serif',
                    'size': 42,
                    'color': 'black'
                },
                "tickfont": {
                    'family': 'Georgia, serif',
                    'size': 42,
                    'color': 'black'
                }
            }
        },
        "unselected": {
            "marker": {
                "opacity": 0.7,
                "size": 2
            }
        },
        "selected": {
            "marker": {
                "opacity": 0.5,
                "size": 25
            }
        },
        "hovertemplate": (
            "<b>WPD Median:</b> %{customdata[0]:.2f} W/m²<br>" +
            "<b>WPD Mean:</b> %{customdata[1]:.2f} W/m²<br>" +
            "<b>GHI Median:</b> %{customdata[2]:.2f} W/m²<br>" +
            "<b>GHI Mean:</b> %{customdata[3]:.2f} W/m²<br>" +
            "<b>Wind Availability:</b> %{customdata[4]:.2f} %<br>" +
            "<b>Solar Availability:</b> %{customdata[5]:.2f} %<br>" +
            "<b>Wind Solar Synergy:</b> %{customdata[6]:.2f} %<br>" +
            "<b>Solar Complements Wind:</b> %{customdata[7]:.2f} %<br>" +
            "<b>Wind Complements Solar:</b> %{customdata[8]:.2f} %<br>" +
            "<b>Wind Episode Lengths:</b> %{customdata[9]:.2f} Hours<br>" +
            "<b>Wind Episode Lulls:</b> %{customdata[10]:.2f} Hours<br>" +
            "<b>Solar Episode Lengths:</b> %{customdata[11]:.2f} Hours<br>" +
            "<b>Solar Episode Lulls:</b> %{customdata[12]:.2f} Hours<br>" +
            "<extra></extra>"
        ),
        "hoverlabel": {
            "font": {
                "size": 32
            }
        },
        "customdata": np.column_stack((
            df['wpd_median'], df['wpd_mean'], df['ghi_median'],
            df['ghi_mean'], df['wpd_availability'], df['ghi_availability'],
            df['wss'], df['scw'], df['wcs'], df['wind_ep_length'], 
            df['wind_ep_lull'], df['solar_ep_length'], df['solar_ep_lull']
        )).tolist(),  # Convert to list for frontend
        "showlegend": False
    }
]
    if clicks > 0 and in_lat is not None and in_lon is not None:

         # Create a marker for the user-provided coordinates
         user_pin = go.Scattermapbox(
             lon=[in_lon],
             lat=[in_lat],
             mode='markers+text',
             marker=dict(size=50, color='white',opacity = 0.6),
             text=["User Location"],
             textposition="top center",
             textfont=dict(size=32, color='white')
         )
         locations.append(user_pin)

    # Add markers for the specified locations
    # pins = [
        # go.Scattermapbox(
        #     lon=cities['latitude'],  # Kutch
        #     lat=cities['longitude'],
        #     mode='markers+text',
        #     marker=dict(size=25, color='navy', opacity = 0.6),
        #     text=cities['City'],
        #     textposition="top center",
        #     textfont=dict(size=32, color='white')
        # )
        # go.Scattermapbox(
        #     lat=cities['latitude'].tolist(),  # Kutch
        #     lon=cities['longitude'].tolist(),
        #     mode='markers+text',
        #     marker=dict(size=15, color='blue', opacity = 0.3),
        #     text=cities['City'].tolist(),
        #     textposition="top center",
        #     textfont=dict(size=32, color='white')
        # )
    # ]

    # Combine the data for the figure
    data = graphData
    # data = locations + pins

    # Return figure
    return {
        'data': data,
        'layout': go.Layout(
            uirevision='foo',  # preserves state of figure/map after callback activated
            hovermode='closest',
            title=title_map[chosen_datastat],
            titlefont=dict(family ='Georgia, serif',size=48, color='black'),  # Customize title font size and color
            # plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
            # paper_bgcolor='rgba(0, 0, 0, 0)',
            title_x=0.5,  # Center the title
            title_y=0.85,  # Adjust vertical position if needed
            hoverdistance=2,
            mapbox=dict(
                style =  "open-street-map",
                center = c,
                zoom = z),
            map=dict(
                style =  "open-street-map",
                center = c,
                zoom = z),
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            showlegend=False
        )
    }