#!/usr/bin/env python3
'''Collection of functions used in the BC Forest Finder notebook.

Usage:
    ./bc-forest-finder.py

Author:
    North Ross - 2025-12-16
'''

def get_starting_geom(starting_location_string, crs=3005):
    """Returns a geopandas.GeoDataFrame object of the geocoded starting location 
    in BC Albers (EPSG:3005) buffered by the defined distance.
    
    Args:
        starting_location_string (str): A string of an address or coordinate that 
            can be recognized by nominatim geocoding service, e.g. "Shirley, BC".
        crs (int): A recognized EPSG code for a coordinate reference system - 
            defaults to BC Albers 3005 but can be edited if needed.
    
    Returns:
        A geopandas.GeoDataFrame object with one row and two columns: 
        'geometry' and 'address' (string of geocoded address).
    """
    import geopandas as gpd
    
    # Prefoorm geocode
    start_point_gdf = gpd.tools.geocode(
        starting_location_string,
        provider="nominatim",
        user_agent="BC_Forest_Finder",
        timeout=10
    )
    # Assert geometry is in BC
    # Convert to BC Albers projection
    start_point_gdf = start_point_gdf.to_crs(crs)
    return start_point_gdf

def get_vri(VRI_where, VRI_fields_dict, start_point_circle, work_dir=':memory:'):
    """Returns a geopandas.GeoDataFrame object of the selected VRI polygons 
    in BC Albers (EPSG:3005), according to the given criteria.
    
    Args:
        VRI_where (str): A string that is appended to the WHERE clause to specify 
            forest type. Cannot be empty
        VRI_fields_dict (dict): A dictionary of VRI fields (keys) and their 
            aliases (values), only the keys are used in this function.
        start_point_circle (geopandas.GeoDataFrame): A geodatagrame containing the
            buffered geometry around the start point.
        work_dir (str): Optional argument to set where to save the duckdb object. 
            By default it works in memory, but this can be set to a 
            directory if working with limited memory or a very large query.
            
    Returns:
        A geopandas.GeoDataFrame object of VRI data based on the given inputs in
        EPSG:3005. 
    """
    import duckdb
    import geopandas as gpd
    # Configure duckdb - install extensions and write location
    conn = duckdb.connect(database = work_dir)
    conn.install_extension("httpfs")
    conn.install_extension("spatial")
    conn.load_extension("spatial")
    conn.load_extension("httpfs")

    # VRI geoparquet object URL
    vri_url = "https://nrs.objectstore.gov.bc.ca/rczimv/geotest/veg_comp_layer_r1_poly.parquet"

    # Convert the buffered starting point to a WKT string
    aoi_str = str(start_point_circle.geometry.iloc[0])

    # Get field names from dict as comma-separated list
    VRI_fields_str = ",".join(VRI_fields_dict.keys())
    
    # Format SQL query
    sql = f"""
    SELECT 
        OBJECTID, ST_AsText(Shape) as wkt, {VRI_fields_str}
    FROM '{vri_url}'
    WHERE 
        ST_Intersects(Shape, ST_GeomFromText('{aoi_str}'))
    AND
        {VRI_where}
    """
    # execute query and convert to pandas dataframe
    df = conn.sql(sql).to_df()

    # convert wkt to geopandas geom
    df['geometry'] = gpd.GeoSeries.from_wkt(df['wkt'])
    df = gpd.GeoDataFrame(df).set_crs(3005, allow_override=True)
    df = df.drop(columns=['wkt'])
    return df
    
def dissolve_adjacent(vri_candidates):
    """Given an input VRI GeoDataFrame, this function will dissolve the entire 
    thing into one record, then explode to split up non-adjacent polygons. 
    After this, the attributes from each polygon will be gathered with a 
    spatial join, then a lambda function is used to aggregate these into a 
    list to display on the final map.
    
    Args:
        vri_candidates (geopandas.GeoDataFrame): A geodateframe object containing VRI data.
    
    Returns: 
        A geopandas.GeoDataFrame similar to the input but with all adjacent 
        (touching) polygons dissolved together with their attributes aggregated.
    """
    
    import geopandas as gpd
    # Dissolve and explode all polygons
    vri_candidates_dissolved = vri_candidates.dissolve().explode()
    # Remove all columns except geom and reset index
    vri_candidates_dissolved = vri_candidates_dissolved[['geometry']].reset_index()
    
    # Perform spatial join with aggregation
    result_gdf = gpd.sjoin(vri_candidates_dissolved, vri_candidates , how='left', predicate='intersects')
    
    # Get columns from VRI query (excluding geometry)
    vri_columns = [col for col in vri_candidates.columns if col != 'geometry']
    # Define dictionary of lambda functions to get unique values for each
    agg_dict = {col: lambda x: ",".join(map(str, set(x.dropna()))) for col in vri_columns}
    # Add geometry preservation
    agg_dict['geometry'] = 'first'
    
    # Aggregate using functions
    aggregated_gdf = result_gdf.groupby(result_gdf.index).agg(agg_dict).reset_index()
    
    # Create a new GeoDataFrame with the aggregated results
    final_gdf = gpd.GeoDataFrame(
        aggregated_gdf, 
        geometry='geometry', 
        crs=vri_candidates.crs
    )
    
    return final_gdf
    
def road_class_to_kmph(road_class):
    """Returns a speed limit value based on road class (OpenStreetMap "highway" 
    tag). This is based on the author's personal experience with BC forest 
    roads and OSM tags.
    
    Note that I am using the "string in string" syntax since sometimes one 
    section has multiple tags. In these cases, the speed from the first 
    condition in the below order will be applied.
    
    Args:
        road_class (str): A string of the "highway" tag from OpenStreetMap tag.
    
    Returns:
        An integer of the max speed for this road in km/h.
    """
    if "primary" in road_class:
        return 70
    elif "secondary" in road_class:
        return 60
    elif "tertiary" in road_class:
        return 50
    elif "residential" in road_class:
        return 50
    elif "unclassified" in road_class:
        return 40
    elif "track" in road_class:
        return 10
    else:
        return 50
        
def get_osm_network(search_radius_km, start_point_gdf):
    """Gets OSM network from a radius around the start point. The search radius is
    buffered to be 30% larger than the radius to search for forest polygons to 
    find routes that are outside the search radius.
    
    Only driving lines are selected, along with OSM lines tagged with 
    "highway"~"track", since these are an important part of BC's forest "road"
    network on OpenStreetMap.
    
    Next, disconnected components are filtered out, the graph is projected to 3005
    and maxspeed is added using the bcforestfinder.road_class_to_kmph() function.
    This is used to calculte travel time and add that to returned network graph.
    
    Args:
        search_radius_km (int): VRI search radius in kilometers
        start_point_gdf (geopandas.GeoDataFrame): A geodataframe object with a
            single point containing the start point from the search, returned by
            the bcforestfinder.get_starting_geom() function.
    
    Returns:
        A networkx.MultiDiGraph object containing all connected roads and tracks 
        to the start point, plus their max speeds and travel times.
    """
    import osmnx as ox
    import networkx as nx
    import geopandas as gpd
    import pandas as pd
    
    # Buffer the search area by an additional 30% of the input search area 
    road_search_radius = (search_radius_km + (0.3 * search_radius_km)) * 1000
    
    # Project the polygon to WGS84 (required by OSMnx)
    road_search_pt = start_point_gdf.to_crs("EPSG:4326").geometry.iloc[0]

    # Define custom network filter: modified from the default "drive" to include tracks, an
    # important part of BC's forest road system (according to OSM)
    # I had to further modify this due to some issues I was having with filtering
    custom_filter = '["highway"~"primary|secondary|unclassified|residential|track"]'

    # Retrieve the network graph
    # I want to include the entre "drive" network plus the "highway=track" features
    # Due to some weirdness with the custom filter, the only way I can find to do this is to 
    # run the function twice with each filter then combine them
    G_drive = ox.graph_from_point(
        center_point = (road_search_pt.y, road_search_pt.x),
        dist = road_search_radius,
        retain_all=True,
        network_type="drive"
    )
    G_track = ox.graph_from_point(
        center_point = (road_search_pt.y, road_search_pt.x),
        dist = road_search_radius,
        retain_all=True,
        custom_filter='["highway"~"track"]'
    )
    graph = nx.compose(G_drive, G_track)
    
    # Remove disconnected segments
    # Get nearest node to center
    central_node = ox.distance.nearest_nodes(graph, 
                                             X=road_search_pt.x, 
                                             Y=road_search_pt.y)
    # Filter to only connected components
    cc = nx.node_connected_component(graph.to_undirected(), central_node)
    graph = graph.subgraph(cc)
    # Reproject to match VRI
    graph = ox.project_graph(graph, to_crs=3005)

    # Make required edits to maxspeed:
    nodes, edges = ox.graph_to_gdfs(graph)
    # Some edges have multiple speed limits. In these cases, pick the first one.
    edges = edges.map(lambda x: x[0] if isinstance(x, list) else x)
    # Separate rows with / without speed limit information 
    mask = edges["maxspeed"].isnull()
    edges_without_maxspeed = edges.loc[mask].copy()
    edges_with_maxspeed = edges.loc[~mask].copy()
    # Apply the function and update the maxspeed
    edges_without_maxspeed["maxspeed"] = edges_without_maxspeed["highway"].apply(road_class_to_kmph)
    # Ensure all the previous maxspeeds are int
    edges_with_maxspeed["maxspeed"] = edges_with_maxspeed["maxspeed"].astype(int)
    # Recombine the two parts
    edges = pd.concat([edges_with_maxspeed, edges_without_maxspeed])

    # Get travel time
    edges["travel_time_seconds"] = edges["length"] / (edges["maxspeed"]/3.6)

    graph = ox.convert.graph_from_gdfs(nodes, edges)
    return graph


def rank_gdf(graph, vri_dissolve, start_point_gdf, max_dist_from_node):
    """Given the dissolved VRI data and the network, this function ranks the 
    candidate polygons by their travel time from the starting point, returning a 
    geodataframe ranked by travel time.
    
    Polygons that are futher than a given linear distance from the nearest node on
    the network are dropped from this output and excluded from analysis. This is 
    to ensure that polygons which are not realistically road-accessible (requiring
    lots of cross-country travel) are not included in the output.
    
    Args:
        graph (networkx.MultiDiGraph): The networkx graph with travel time given 
            by bcforestfinder.get_osm_network()
        vri_dissolve (geopandas.GeoDataFrame): The candidate VRI polygons given
            by bcforestfinder.dissolve_adjacent()
        start_point_gdf (geopandas.GeoDataFrame): A geodataframe object with a
            single point containing the start point from the search, returned by
            the bcforestfinder.get_starting_geom() function.
        max_dist_from_node (int): The maximum linear distance in meters between 
            the nearest node on the network and a candidate VRI polyon before it
            is discarded from analysis.
            
    Returns:
        A geopandas.GeoDataFrame() similar to the vri_dissolve input with ranking,
        network node list path, travel time, road distance, track distance and 
        cross-country distance appended.
    """
    import osmnx as ox
    import networkx as nx
    import geopandas as gpd
    import pandas as pd
    
    # Get nearest graph nodes to central point and polygon centroids
    central_node = ox.distance.nearest_nodes(graph, 
                                             X=start_point_gdf.geometry.x, 
                                             Y=start_point_gdf.geometry.y)
    
    polygon_distances = []
    
    for index, polygon in vri_dissolve.iterrows():
        try:
            # Get polygon centroid
            poly_centroid = polygon.geometry.centroid
            
            # Find nearest graph node to polygon centroid
            dest_node = ox.distance.nearest_nodes(graph, 
                                                    X=poly_centroid.x, 
                                                    Y=poly_centroid.y,
                                                    return_dist=True)
            # Discard polygon if it is longer than max_distance_from_node from node
            if dest_node[1] > max_dist_from_node:
                print(f"Discarded candidate {dest_node[1]/1000:.3f}km from node")
                raise nx.NetworkXNoPath
            # Calculate shortest path length
            # try:
            path = nx.dijkstra_path(graph, 
                                     source=central_node[0], 
                                     target=dest_node[0], 
                                     weight='travel_time_seconds')
            # Get gdf of path route
            route_gdf = ox.routing.route_to_gdf(graph, path) 
            
            # Get total distance
            distance = route_gdf.length.sum()
            # Get track distance
            track_distance = route_gdf.loc[route_gdf['highway']=='track'].length.sum()
            # Get non-track road distance
            road_distance = route_gdf.loc[route_gdf['highway']!='track'].length.sum()
            # Get total travel time
            travel_time_seconds = route_gdf["travel_time_seconds"].sum()
            
            polygon_distances.append({
                'polygon_id': index,
                'path': path,
                'distance': distance,
                'track_dis': track_distance,
                'road_dis': road_distance,
                'travel_time_seconds': travel_time_seconds,
                'Cross-Country Distance': dest_node[1]
            })
        # Handle polygons that could not be routed to
        except nx.NetworkXNoPath: 
            polygon_distances.append({
                'polygon_id': index,
                'path': None,
                'distance': None,
                'track_dis': None,
                'road_dis': None,
                'travel_time_seconds': None,
                'Cross-Country Distance': dest_node[1]
            })

    # Create dataframe and rank based on total distance
    df = pd.DataFrame(polygon_distances)
    df['rank'] = df['travel_time_seconds'].rank(method='first')
    return df

def getFoliumMap(top_candidates, VRI_fields_dict, graph, start_point_gdf):
    """Creates a folium.Map() object (leaflet map) based on the top candidates 
    returned from the analysis. This is symbolized based on the ranking and shows
    the candidate polygons and their paths on a satellite image background. The 
    polygons contain popups with additional attributes.
    
    Args:
        top_candidates (geopandas.GeoDataFrame): A GeoDataFrame containing the top
            ranked VRI candidate polygons by travel time.
        VRI_fields_dict (dict): A dictionary containing the field names (keys) and
            aliases (values) to use for labelling the popups.
        graph (networkx.MultiDiGraph): The NetworkX graph object used for drawing
            the path lines in the output.
        start_point_gdf (geopandas.GeoDataFrame): A geodataframe object with a
            single point containing the start point from the search, returned by
            the bcforestfinder.get_starting_geom() function. This will be 
            displayed as a red dot on the output.
    Returns:
        folium.Map object.
    """
    import folium
    import branca.colormap as cm
    import osmnx as ox
    from shapely import LineString
    
    m = folium.Map(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite View',
        control_scale = True
    )
    # Create colormap for legend based on max and min rank
    color_map = cm.LinearColormap(
        colors=['#2196F3', "#b0fffb", '#FF9800'],
        vmin=top_candidates['rank'].min(),
        vmax=top_candidates['rank'].max()
    )
    
    # Create fields and alias lists for popups:
    fields_list = ['rank', 'distance', 'travel_time_seconds']
    fields_list.extend(list(VRI_fields_dict.keys()))
    aliases_list = ['Rank', 'Distance (m)', 'Travel Time (s)']
    aliases_list.extend(list(VRI_fields_dict.values()))

    # Define style functions based on attributes
    def style_function_polys(feature):
        return {
            'color': color_map(feature["properties"]['rank']),
            'weight': 1,
            'fillOpacity': 0.1
        }
    def get_dash_array(highway):
        if highway == 'track':
            return '6, 6' # dashed lines for tracks
        elif highway == 'trackless':
            return '2, 5' # fine dash line for trackless
        else:
            return '1, 0' # all else give solid line
    def style_function_roads(feature):
        return {
            'color': color_map(feature["properties"]['rank']),
            'weight': 2,
            'fillOpacity': 0.1,
            'dashArray': get_dash_array(feature["properties"]['highway'])
        }
    # Reverse order so that the highest-ranking lines/polys draw over the lowest ones
    top_candidates = top_candidates.sort_values('rank', ascending=False)
    # Convert top candidates to JSON and add to map
    json = top_candidates.to_json(default=str, to_wgs84=True)
    folium.GeoJson(
        json,
        style_function = style_function_polys,
        popup = folium.GeoJsonPopup(
            fields = fields_list,
            aliases = aliases_list
        )
    ).add_to(m)
    
    # Add the paths to each one in the same color:
    for i, row in top_candidates.iterrows():
        # Get path to the given candidate as gdf
        line_gdf = ox.routing.route_to_gdf(graph, row['path'])
        
        # Extend the line to the polygon centroid
        # Get last coordinate of last line
        last_node = line_gdf.iloc[len(line_gdf)-1].geometry.coords[-1]
        # Get polygon centroid
        poly_centroid = row.geometry.centroid
        # Add a new line connecting the two
        line_gdf.loc[len(line_gdf), ['geometry', 'highway']] = [LineString([last_node, poly_centroid]), 'trackless']
        
        # add the rank from the current candidate
        line_gdf['rank'] = row['rank']
        
        # Convert to JSON, style and add to map
        line_json = line_gdf.to_json(default=str, to_wgs84=True)
        folium.GeoJson(line_json, style_function = style_function_roads).add_to(m)

    # Add the starting location as a red dot
    start_pt = start_point_gdf.to_crs("EPSG:4326").geometry.iloc[0]
    folium.CircleMarker(
        location=[start_pt.y, start_pt.x],
        radius=7,  # size of the circle
        color='white',
        fill=True,
        fillColor='red',
        fillOpacity=0.7
    ).add_to(m)

    # Create custom HTML legend
    box_height = 210 + (color_map.vmax*20)
    legend_html = f'''
    <div style="position: fixed; 
                top: 30px; right: 5px; width: 220px; height: {box_height}px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px;">
        <p><b>Forest Polygon Rank</b></p>
    '''
    # Add color gradient
    for i in range(int(color_map.vmax)):
        rank  = i+1
        relative_value = i / (int(color_map.vmax) - 1)
        color = color_map(color_map.vmin + relative_value * (color_map.vmax - color_map.vmin))
        legend_html += f'''
            <div style="display: flex; align-items: center; margin-bottom:5px;">
                <div style="width: 30px; text-align: right; margin-right: 10px;">
                    {rank}
                </div>
                <div style="background-color:{color}; width: 80px; height:20px;"></div>
            </div>
        '''
    # Add line patterns and starting location
    color_1 = color_map(1)
    legend_html += f'''
        <p><b>Road Types</b></p>
        <svg height="60" width="220">
            <line x1="10" y1="10" x2="60" y2="10" 
                  stroke="{color_1}" stroke-width="2" stroke-dasharray="1,0"/>
            <text x="70" y="15">Road</text>
            
            <line x1="10" y1="30" x2="60" y2="30" 
                  stroke="{color_1}" stroke-width="2" stroke-dasharray="6, 6"/>
            <text x="70" y="35">Track</text>
            
            <line x1="10" y1="50" x2="60" y2="50" 
                  stroke="{color_1}" stroke-width="2" stroke-dasharray="2,5"/>
            <text x="70" y="55">Cross-Country</text>
        </svg>
        <p><b>Start Location</b></p>
        <svg height="15" width="220">
            <circle cx="20" cy="7.5" r="7" 
                    stroke="white" stroke-width="1" 
                    fill="red" fill-opacity="0.7"/>
            <text x="70" y="13">Start location</text>
    </div>
    '''
    # Add legend to map
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Fit to data
    folium.FitOverlays().add_to(m)
    return m