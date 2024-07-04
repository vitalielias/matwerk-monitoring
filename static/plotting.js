function fetchAndPlot(plotName, organization = null, resource_type = null) {
    let startTime = performance.now();

    let plotDiv = document.getElementById(`plot-${plotName}`);
    let cardDiv = plotDiv.closest('.card');

    let url = new URL(`/plot/${plotName}`, window.location.origin);
    if (organization !== null) {
        url.searchParams.append('organization', organization);
    }
    if (resource_type !== null) {
        url.searchParams.append('resource_type', resource_type);
    }

    startLoading(cardDiv);

    fetch(url)
        .then(response => {
            let endTime = performance.now();
            let timeElapsed = endTime - startTime;

            if (!response.ok) {
                throw response;
            }
            showInfoMessage(cardDiv, `Plot generated in ${timeElapsed.toFixed(2)} ms`);
            return response.json();
        })
        .then(data => {
            hideSpinner(cardDiv);
            showPlot(cardDiv);
            Plotly.newPlot(`plot-${plotName}`, data);
        })
        .catch(response => {
            if (response.status === 404) {
                response.json().then(data => {
                    hideSpinner(cardDiv);
                    showError(cardDiv, data.error);
                });
            } else {
                console.error('Error:', response);
                console.log(`Fetch operation failed for plot: ${plotName}`);
            }
        });
}

function fetchDataFrame(dataframe_name) {
    let startTime = performance.now();

    let df_div = document.getElementById(`df-${dataframe_name}`);
    let cardDiv = df_div.closest('.card');

    let url = new URL(`/table/${dataframe_name}`, window.location.origin);
    startLoading(cardDiv);

    fetch(url)
        .then(
            response => {
                let endTime = performance.now();
                let timeElapsed = endTime - startTime;

                if (!response.ok) {
                    throw response;
                }
                showInfoMessage(cardDiv, `Table loaded in ${timeElapsed.toFixed(2)} ms`);
                return response.json();
            }
        )
        .then(data => {
            hideSpinner(cardDiv);

            // replace the inner html of the table div with the new data
            df_div.innerHTML = data.html;
        })
        .catch(error => {
            hideSpinner(cardDiv);
            showError(cardDiv, `Failed to fetch table ${dataframe_name}`);
            console.error('Error:', error);
        });
}

function startLoading(cardDiv) {
    hidePlot(cardDiv);
    showSpinner(cardDiv);
    hideError(cardDiv);
    hideInfoMessage(cardDiv);
}

function hidePlot(cardDiv) {
    let plotDiv = cardDiv.querySelector('.plot-container');
    // This is here for a different reason than the hideSpinner function. We use this same function
    // for both plots and dataframes. Dataframe cards don't have a plotDiv.
    if (plotDiv != null) {
        plotDiv.classList.add('d-none');
    }
}

function showPlot(cardDiv) {
    let plotDiv = cardDiv.querySelector('.plot-container');
    plotDiv.classList.remove('d-none');
}

function showSpinner(cardDiv) {
    let spinner = cardDiv.querySelector('.spinner');
    // There is an instance where the spinner is not present in the card div at the time the
    // first time the function is called. I'm not clear on why this is happening.
    if (spinner != null) {
        spinner.classList.remove('d-none');
    }
}

function hideSpinner(cardDiv) {
    let spinner = cardDiv.querySelector('.spinner');
    spinner.classList.add('d-none');
}

function showError(cardDiv, message) {
    let errorDiv = cardDiv.querySelector('.error.message');
    errorDiv.textContent = message;
    errorDiv.classList.remove('d-none');
}

function hideError(cardDiv) {
    let errorDiv = cardDiv.querySelector('.error.message');
    if (errorDiv !== null) {
        errorDiv.textContent = '';
        errorDiv.classList.add('d-none');
    }
}

function showInfoMessage(cardDiv, message) {
    let infoDiv = cardDiv.querySelector('.info.message');
    if (infoDiv !== null) {
        infoDiv.textContent = message;
        infoDiv.classList.remove('d-none');
    }
}

function hideInfoMessage(cardDiv) {
    let infoDiv = cardDiv.querySelector('.info.message');
    if (infoDiv !== null) {
        infoDiv.textContent = '';
        infoDiv.classList.add('d-none');
    }
}

