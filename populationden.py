import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Population Density of Kenya Report 2019 Census'
APP_SUB_TITTLE = 'Source:The Kenya National Bureau of Statistics is the department in Kenyas Ministry of Planning'

# Define the population_density_facts function
def population_density_facts(df, county, field_name, metric_title):
    if county == '':
        # show whole DataFrame without any filters
        df_filtered = df
    else:
        # filter DataFrame based on county
        df_filtered = df[df['County'] == county]
    
    total = df_filtered[field_name].sum()
    st.metric(metric_title, total)

def display_map(df, county, field_name):
    if county == '':
        # show whole DataFrame without any filters
        df_filtered = df
    else:
        # filter DataFrame based on county
        df_filtered = df[df['County'] == county]
    
    # Convert Total_Population19 column to float
    df_filtered['Population Density'] = df_filtered['Population Density'].str.replace(',', '').astype(float)

    # Replace NaN values with 0
    df_filtered['Population Density'].fillna(0, inplace=True)

    # Define Folium Scale
    threshold_scale = [0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, df_filtered['Population Density'].max()]
    
    # rest of the code ...

    #TYING THE COUNTY NAME IN CSV WITH THE COUNTY NAME OF THE GEOJSON FILE SHAPEFILES
    map = folium.Map(location=[0.0236, 37.9062], zoom_start=5.5, scrollWheelZoom=False, tiles='CartoDB positron')
    choropleth=folium.Choropleth(
        geo_data= r'C:\Users\Njuguna\Downloads\Population Density\Kenyaadm.json',
        data=df_filtered,
        columns=['County', 'Population Density'],
        key_on='feature.properties.NAME_1',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        threshold_scale=threshold_scale,
        highlight=True,
    )
    choropleth.geojson.add_to(map)

    df = df.set_index('County')
    county_name = 'Baringo'

    for feature in choropleth.geojson.data['features']:
        county_name = feature['properties']['NAME_1']
        
    choropleth.geojson.add_child(
        folium.GeoJsonTooltip(["NAME_1"], labels=False)
    )
    
    #DISPLAYS size of the Folium map
    st_map = st_folium(map, width=700, height=450)

    #DISPLAYS NAME OF POLYGON ONCE CLICKED
    if st_map["last_active_drawing"]:
        st.write(st_map["last_active_drawing"]['properties']['NAME_1'])

    st.write(df.shape)    
    st.write(df.head())


    

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=None, layout='wide', initial_sidebar_state='auto')

    st.title(APP_TITLE)
    st.subheader(APP_SUB_TITTLE)

    #Load Data
    df_continental = pd.read_csv(r'C:\Users\Njuguna\Downloads\Population Density\pop20.csv')
    df = pd.read_csv(r'C:\Users\Njuguna\Downloads\Population Density\pop20.csv')

    county = ''

    field_name = 'Total_Population19'
    metric_title = f'# {field_name} Reports'

    population_density_facts(df, county, field_name, metric_title)

    
    #Display Filters and Map

    display_map(df_continental, county, field_name )

    #Display Metrics

if __name__ == "__main__":
    main()
