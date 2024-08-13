# RPDM Dashboard Template

## Introduction

This project serves as the main frontend interface of the monitoring dashboard currently in development for serving usage metrics and KPIs about KIT-developed MatWerk services to a GUI, and is built using Flask and Jinja2. It has been adapted from a similar visualization dashboard for the [Coscine RDM platform](https://coscine-reporting.otc.coscine.dev/), with the main template source code available [here](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/tree/main).

## Installation

This project requires Python 3.11 or higher in order to run.

### Poetry

This project uses Poetry to manage dependencies. To install Poetry, refer to the
[official documentation](https://python-poetry.org/docs/#installation).

To install the dependencies, run the following command:

```bash
poetry install
```

### Pip

If you prefer to use pip, you can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

### Poetry with an Isolated Environment

This is my preferred method, just to keep projects seperate. 

```bash
poetry config virtualenvs.in-project true  # Create the .venv directory in the project directory
poetry shell  # Create a shell locally to work with
```

Then, inside the shell

```bash
poetry install  # Install our dependencies there instead of our main environment
exit  # To leave the shell and return to our base environment
```

And to run the application:
```bash
poetry run python app.py
```


## Running the Application

To run the application, execute the following command:

```bash
python app.py
```

The application will be available at [http://localhost:3838](http://localhost:383).

## Adding New Plots

In [index.html](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/templates/index.html.j2) there's a div with the id `card-container`. This div is a [bootstrap row](https://getbootstrap.com/docs/5.0/layout/grid/), and all of the elements within will automatically orient themselves within. 

Plots are generated using the [Plotly JavaScript Library](https://plotly.com/javascript/). We provide the nessecary JSON to build the plot via the [`/plot/<plot_name>` endpoint in app.py](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/app.py#L28-54). 

We can add a new plot to the page by calling the `plot_card` macro, which comes from the [templates/components/cards.html.j2](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/templates/components/card.html.j2) file. This macro accepts five parameters:

- `plot_name` (required): The name of the plot. For simplicity, this is the same name as is passed into the `/plot/<plot_name>` endpoint.
- `title` (required): The name that should appear at the top of the card.
- `icon`: The [font-awesome](https://fontawesome.com/icons) icon that should appear next to the title. Typically, this reflects the kind of plot being rendered.
- `large`: If true, creates a double width card.
- `height`: Set the height of the card in pixels.

## Adding New Tables

Table data is expected to be returned as an html table with the "dataframe" class (this is automatically applied by pandas when calling `DataFrame.to_html()`). Typically, we also include the classes "table table-condensed" for some automatic styling. You can also add the class "sum", which bolds and highlights the last row of the table.

Similarly to plots, we can add a new macro to the `card-container` div, this time using the `draw_table` macro. This macro only takes two variables:

- `dataframe_name` (required): The name of the dataframe. As in `plot_card`, this value is passed directly to the [`/table/<table_name>` endpoint in app.py](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/app.py#L58-76)
- `title` (required): The name that should appear at the top of the card.
- `large`: If true, creates a double width card.
- `height`: Set the height of the card in pixels.

## Adding New Pages

The simplist way to add a new page would be to just add another file in the [templates](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/tree/main/templates) directory and create a new endpoint in [app.py](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/app.py) to render it.

In order to link to the new page, you'll need to add the relative path to the side nav bar by editing the [templates/partials/side_nav.html.js](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/templates/partials/side_nav.html.j2)

## Adding New Scripts / Styles

New scripts and styles can be added to the [static](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/tree/main/static) folder, then referenced in the [templates/partials/head.html.j2](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/templates/partials/head.html.j2) or [templates/partials/scripts.html.j2](https://git.rwth-aachen.de/jonathan.a.hartman1/rpdm-dashboard-template/-/blob/main/templates/partials/scripts.html.j2) as appropriate.


# Services to Monitor and their respective metrics


| Metric                                | Description                                                                                               | Implementation Approach                                                                                   | Effort Required  | Tools Applicable                                                                                                                                                                                                                     |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Users**                      | Number of users using the tool over a specific period of time                                          | Implement user tracking via IP or authentication.                                  | Low              | <ul><li>- [x] EVOKS</li><li>- [x] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [x] Matwerk Data repository</li><li>- [x] Matwerk Metadata repository</li><li>- [x] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Location of Users**                 | Geographic distribution of users.                                                                         | Use an IP geolocation API (e.g., country.is) to determine user locations. Store location data with user session information.                     | Low              | <ul><li>- [x] EVOKS</li><li>- [x] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [x] Matwerk Data repository</li><li>- [x] Matwerk Metadata repository</li><li>- [x] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Processed Gigabytes of Images**     | Total amount of data processed by the tool.                                                               | Log the file size of each batch processed in the backend. Aggregate this data periodically to get total processed file sizes.                    | Medium           | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Number of Extractions/ Mappings**   | Count of metadata extractions and mappings completed.                                                     | Increment a counter in the backend each time an extraction/mapping process is completed successfully. Store the counts in a database for reporting. | Low              | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Processing Time per Image**         | Average time taken to process each image.                                                                 | Record timestamps at the start and end of each image processing task. Calculate and log the processing time for each task.                      | Low              | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **User Engagement**                   | Average session duration and actions taken per session.                                                   | Use frontend analytics tools (e.g., Google Analytics) to track user interactions and session durations.                                         | Medium           | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Schema/Plugin Usage**               | Frequency of usage of different schemas/plugins.                                                          | Log the schema/plugin selected by users for each extraction/mapping task. Store and analyze this data to understand schema/plugin popularity.     | Low              | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Repeat Usage**                      | Number of users returning to use the tool multiple times.                                                 | Implement user authentication and track user IDs or session tokens across multiple sessions. Store and analyze data to identify repeat usage patterns. | Low              | <ul><li>- [x] EVOKS</li><li>- [x] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [x] Matwerk Data repository</li><li>- [x] Matwerk Metadata repository</li><li>- [x] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **API Response Times**                | Average response time of the tool's API.                                                                  | Implement API performance monitoring to track response times and log this data.                                                                 | Low              | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Documentation Access**              | Frequency of access to help or documentation pages.                                                       | Track page views or clicks on documentation/help sections using analytics tools.                                                                | Low              | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |
| **Number of Plugins**                 | Simple count of the available mappings                                                                    | Could also be done manually                                                                                 | Low              | <ul><li>- [ ] EVOKS</li><li>- [ ] SKOSMOS</li><li>- [x] Mapping Service</li><li>- [ ] Matwerk Data repository</li><li>- [ ] Matwerk Metadata repository</li><li>- [ ] FAIRDOScope, data collections explorer, other DEM tools beyond MatWerk</li></ul> |

