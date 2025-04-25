import streamlit as st
import pandas as pd
import altair as alt

# Set the page configuration to wide layout
st.set_page_config(layout="wide")
st.title("Mass Shootings over the years in USA interactive visualizations")
st.markdown("### By Laura Humet and Maria Sans")
st.write("Upload the CSV file with the necessary data, following the instructions below.")

# File uploader for the gun violence data
uploaded_file = st.file_uploader("Choose the shootings.csv file, please", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Load the CSV data into a DataFrame
    shootings = pd.read_csv(uploaded_file)

    
    shootings = shootings.rename(columns = {'County Name':'County'})
    shootings['mass_shootings_per_state'] = shootings.groupby(['Incident Year', 'State'])['State'].transform('count')
    shootings['mass_shootings_per_region'] = shootings.groupby(['Incident Year', 'Region'])['Region'].transform('count')
    shootings['mass_shootings_per_county'] = shootings.groupby(['Incident Year', 'County'])['County'].transform('count')

    # Real population per region based on recent estimates
    population_per_region_dict = {
        'Northeast': 57700000,
        'Midwest': 68600000,
        'Southwest': 10200000,
        'Southeast': 26500000,
        'Northwest': 13300000
    }

    # Map the population per region from the dictionary
    shootings['Population per Region'] = shootings['Region'].map(population_per_region_dict)

    import altair as alt
    from vega_datasets import data

    # Define selection for the region and for the year
    region_selection = alt.selection_point(fields=['Region'])

    year_range = {'x': [shootings['Incident Year'].min(), shootings['Incident Year'].max()]}
    year_selection = alt.selection_interval(encodings=['x'], value=year_range)

    state_selection = alt.selection_point(fields=['State', 'FIPS_State'], empty='none')

    from vega_datasets import data
    import numpy as np

    map = alt.topo_feature(data.us_10m.url, 'states')

    ## REGION CHARTS ##
    map_regions = alt.Chart(map).mark_geoshape().encode(
        color = alt.condition(region_selection, alt.Color('Region:N').legend(title='Regions'), alt.value('#EEEEEE')),
        stroke = alt.value('lightgray'),
        tooltip = alt.Tooltip('Region:N')
    ).transform_lookup(
        lookup = 'id',
        from_ = alt.LookupData(shootings, 'FIPS_States', ['Region'])
    ).transform_filter(
        alt.datum.Region != None
    ).add_params(
        region_selection
    ).properties(
        width = 250,
        height = 150
    ).project('albersUsa')

    regions_chart = alt.Chart(shootings).mark_line(strokeWidth = 3).encode(
        x = alt.X('Incident Year:N', axis = alt.Axis(title = 'Year'), scale=alt.Scale(nice=False, padding=10)).scale(domain=year_selection),
        y = alt.Y('mass_shootings_per_100k_per_region:Q', axis = alt.Axis(title = 'Mass Shootings'), scale=alt.Scale(nice=False, padding=10)),
        color = alt.Color('Region:N').legend(title='Regions'),
        opacity=alt.condition(region_selection, alt.value(1.0), alt.value(0.1)),
        tooltip=[alt.Tooltip('Region:N', title='Region'), alt.Tooltip('mass_shootings_per_100k_per_region:Q', title='Mass Shootings per 100k citizens', format=".2f")]
    ).transform_calculate(
        mass_shootings_per_100k_per_region="datum.mass_shootings_per_region / datum['Population per Region'] * 100000"
    ).transform_filter(
        year_selection
    ).add_params(
        region_selection
    ).properties(
        width = 250,
        height = 150
    )
    regions = alt.vconcat(map_regions, regions_chart, title={'text':['Evolution of Mass Shootings per 100k citizens in the US by regions'],
                                                            'subtitle':'Select a region'})

    ## STATE CHARTS ##
    map_states = alt.Chart(map).mark_geoshape().encode(
        color=alt.condition(state_selection, alt.Color('State:N').legend(title='States'), alt.value('#EEEEEE')),
        stroke = alt.value('lightgray'),
        tooltip = alt.Tooltip('State:N')
    ).transform_lookup(
        lookup = 'id',
        from_ = alt.LookupData(shootings, 'FIPS_States', ['State', 'Region'])
    ).transform_filter(
        alt.datum.State != None
    ).transform_filter(
        region_selection
    ).add_params(
        state_selection, region_selection
    ).properties(
        width = 250,
        height = 150
    ).project('albersUsa')

    states_chart = alt.Chart(shootings).mark_line(strokeWidth = 3).encode(
        x = alt.X('Incident Year:N', axis = alt.Axis(title = 'Year'), scale=alt.Scale(nice=False, padding=10)).scale(domain=year_selection),
        y = alt.Y('mass_shootings_per_100k_per_state:Q', axis = alt.Axis(title = 'Mass Shootings'), scale=alt.Scale(nice=False, padding=10)),
        color = alt.Color('State:N').legend(title='States'),
        opacity=alt.condition(state_selection, alt.value(1.0), alt.value(0.05)),
        tooltip=[alt.Tooltip('State:N', title='State'), alt.Tooltip('mass_shootings_per_100k_per_state:Q', title='Mass Shootings per 100k citizens', format=".2f")]
    ).transform_calculate(
        mass_shootings_per_100k_per_state = "datum.mass_shootings_per_state / datum['Population per State'] * 100000"
    ).transform_filter(
        region_selection
    ).transform_filter(
        year_selection
    ).add_params(
        state_selection, region_selection
    ).properties(
        width = 250,
        height = 150
    )

    states = alt.vconcat(map_states, states_chart, title={'text':['Evolution of Mass Shootings per 100k citizens in the US', 'for each state of the selected region'],
                                                        'subtitle': 'Select a state'})

    ## COUNTY CHARTS ##
    counties_chart = alt.Chart(shootings).mark_line(strokeWidth = 2, point={'size': 100}).encode(
        x = alt.X('Incident Year:N', axis = alt.Axis(title = 'Year'), scale=alt.Scale(nice=False, padding=10)).scale(domain=year_selection),
        y = alt.Y('mass_shootings_per_100k_per_county:Q', axis = alt.Axis(title = 'Mass Shootings'), scale=alt.Scale(nice=False, padding=10)),
        color = alt.Color('County:N', legend=alt.Legend(
                title='Counties',
                orient='right',
                offset=10,
                format=alt.condition(state_selection, alt.value('visible'), alt.value('none'))
            )),
        tooltip=[alt.Tooltip('County:N', title='Counties'), alt.Tooltip('mass_shootings_per_100k_per_county:Q', title='Mass Shootings per 100k citizens', format=".2f")]
    ).transform_calculate(
        mass_shootings_per_100k_per_county="datum.mass_shootings_per_county / datum['Population per County'] * 100000"
    ).transform_filter(
        state_selection
    ).transform_filter(
        year_selection
    ).transform_filter(
        alt.datum.mass_shootings_per_county >= 3
    ).add_params(
        state_selection
    ).properties(
        width = 200,
        height = 200,
        title={
            'text':['Evolution of Mass Shootings per 100k citizens in the US', 'for each county in the selected state'],
            'subtitle':'(At least 3 mass shootings per county)'
            }
    )

    year_selection_chart = alt.Chart(shootings, width=600, height=60).mark_line().encode(
        x = alt.X('Incident Year:N', title='Year'),
        y = alt.Y('mass_shootings_per_region:Q', title=None),
        color = alt.Color('State:N', legend=None)
    ).add_params(
        year_selection
    ).properties(
        width=200,
        height=40,
        title={
            "text": "Select Year Range",
            "subtitle": "Drag across the years below to select the range of interest."
        }
    )


    counties_and_years = alt.vconcat(counties_chart, year_selection_chart).resolve_scale(color='independent')

    final_chart = alt.hconcat(regions, states, counties_and_years).resolve_scale(color='independent')

    st.altair_chart(final_chart, use_container_width=True)



    # Calculate "Shootings per Capita" first
    shootings['Shootings per Capita'] = 1 / shootings['Population per Region']

    # Calculate "Shootings per 100k"
    shootings['Shootings per 100k'] = shootings['Shootings per Capita'] * 100000  # Scale to 100,000 citizens

    # Aggregate by Region and Year
    region_year_data = shootings.groupby(['Region', 'Incident Year', 'Population per Region']).agg(
        shootings_per_100k=('Shootings per 100k', 'sum')  # Sum of shootings per 100k
    ).reset_index()

    # Define selection for the region and year
    region_selection = alt.selection_point(fields=['Region'])
    year_range = {'x': [shootings['Incident Year'].min(), shootings['Incident Year'].max()]}
    year_selection = alt.selection_interval(encodings=['x'], value=year_range)
    state_selection = alt.selection_point(fields=['State'])

    shootings['mass_shootings_per_state'] = shootings.groupby(['Incident Year', 'State'])['State'].transform('count')
    shootings['mass_shootings_per_region'] = shootings.groupby(['Incident Year', 'Region'])['Region'].transform('count')
    shootings['mass_shootings_per_county'] = shootings.groupby(['Incident Year', 'County'])['County'].transform('count')

    
    # Identify the first year in the dataset for the slope chart
    first_year = region_year_data['Incident Year'].min()

    # Filter years to include only the first year and years from first_year + 1 onwards
    valid_years = region_year_data[region_year_data['Incident Year'] > first_year]['Incident Year'].unique()

    # Create a dropdown filter for year selection for the slope chart
    year_dropdown = alt.binding_select(
        options=sorted(valid_years),
        name="Select Year: "
    )

    year_select = alt.selection_point(fields=["Incident Year"], bind=year_dropdown, value=2015, name='year_select')

    slope_chart = alt.Chart(region_year_data,  width=800, height=600).transform_calculate(
        is_selected_or_first_year="datum['Incident Year'] == " + str(first_year) + " || datum['Incident Year'] == year_select['Incident Year'][0]"
    ).mark_line(point=True).encode(
        x=alt.X('Incident Year:N', title="Year"),
        y=alt.Y('shootings_per_100k:Q', title="Shootings per 100,000 Citizens"),
        color=alt.Color('Region:N', legend=alt.Legend(title="Region")),
         tooltip=[
        'Region:N', 
        'Incident Year:O', 
        alt.Tooltip('shootings_per_100k:Q', title="Shootings per 100k", format=".2f"), 
        alt.Tooltip('Population per Region:Q', title="Population", format=",")  
    ]
    ).transform_filter(
        "toBoolean(datum.is_selected_or_first_year)"
    ).add_params(
        year_select
    ).properties(
        title="Change in Shootings per 100,000 Citizens Across Regions Compared to First Year"
    )

        # Add points with size adjustment
    points = slope_chart.mark_point(filled=True, size=200)

    # Combine the line and points
    slope_chart = slope_chart + points


    # Display the slope chart last
    st.markdown("## Evolution of Mass Shootings Across Regions Compared to the First Year (2014)")
    st.altair_chart(slope_chart)
    st.write("In the dropdown menu above, select the year you want to compare with the first year")
