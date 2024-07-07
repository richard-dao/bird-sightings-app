# Using the Bird Watching App

Watch the demo here:
https://github.com/richard-dao/bird-sightings-app/blob/main/Bird-Sighting-App-Demo.mp4

Welcome to the Bird Watching App! This guide will help you navigate and utilize the app's various features, inspired by [ebird.org](https://ebird.org). The app is designed to provide a seamless experience for bird enthusiasts, offering tools for viewing bird densities, submitting checklists, exploring birding locations, and more.

The app is organized into several main pages:

- **Index Page**: Displays a welcoming interface with a bird density map.
- **Checklist Page**: Allows you to enter your bird sightings.
- **Stats Page**: Shows statistics and compilations of your birding data.
- **Location Page**: Provides detailed information about specific birding locations.

## Index Page

Upon logging in, you'll be greeted by the Index Page. Here’s what you can do:

- **View Bird Density Map**: The map centers on your region, displaying bird density. Use the map controls to zoom in/out and pan to different areas.
- **Select a Bird Species**: Use the species selection box to choose a specific bird. The map will update to show the density of the selected species. If no species is chosen, the map will show data for all birds.
- **Draw a Region**: Draw a rectangle on the map to select a specific area. Click the "Statistics on Region" button to see detailed statistics for that area on the Stats Page.
- **Navigation Links**: Access the Checklist Page to submit your bird sightings or the Stats Page to view your personal birding statistics.

### Map Features
#### Using Leaflet

The map functionality allows you to interact with bird density data by creating a heatmap using Leaflet.js.
### Species Selection

To filter the map data by bird species:

- **Search Box**: Type the name of a bird in the search box with autocomplete. The map updates to show densities for the selected species.
- **Default View**: If no species is selected, the map shows data for all species.

## Checklist Page

On the Checklist Page, you can record your bird sightings:

- **Accessing the Page**: From the Index Page, select a location on the map and click "Enter Checklist".
- **Species Search**: Use the search bar to find and select a species. For instance, typing "spar" will filter to show sparrows.
- **Record Sightings**: For each species, enter the number of birds seen in the respective field. Use the increment button to adjust the count.
- **Submit Checklist**: Once you’ve entered all your sightings, click "Submit" to save your checklist.

Additionally, you can view and manage your submitted checklists on the "My Checklists" page. Here, you can edit or delete entries as needed.

## Location Page

To explore birding locations in more detail:

- **Selecting a Region**: On the Index Page, draw a rectangle on the map and click "Region Information" to navigate to the Location Page.
- **Statistics Overview**: View a list of species seen in the selected region, along with the number of checklists and total sightings.
- **Species Graphs**: Click on any species in the list to display a graph showing the number of birds seen over time.
- **Top Contributors**: See information about the top bird watchers in the region.

To create these visualizations, we use [Chart.js](https://www.chartjs.org/).

## User Statistics

On the Stats Page, you can view detailed statistics about your bird-watching activities:

- **Species List**: See a searchable list of all species you have observed. Clicking on a species provides visualizations of when and where you saw it.
- **Trends Over Time**: Explore how your bird-watching habits have changed over time with various graphical representations.


### Sample Data

We initialize the database with sample data provided [here](https://drive.google.com/drive/folders/1NV5vMn0h3O5peppvBHqcdJAudPQe_Qkg?usp=sharing). The data includes:

- **species.csv**: Contains about 400 bird species.
- **checklists.csv**: Includes checklists with user, location, and date details.
- **sightings.csv**: Lists sightings with a checklist ID, species, and count.

These files can be loaded into the database using Python's `csv` module. The data is sourced from modified eBird checklists to serve as realistic, albeit synthetic, examples for this app.

Happy bird watching!
