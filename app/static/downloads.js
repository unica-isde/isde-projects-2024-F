function downloadPLOT(elementID) {
    /**
     *  The downloadPLOT function captures the content of an HTML canvas element and allows
     *  the user to download it as an image file in JPEG format. If the specified
     *  canvas element does not exist, an alert notifies the user, and the
     *  function terminates. The function retrieves the canvas using its ID
     *  and extracts its contents using toDataURL("image/jpeg"), converting
     *  it into a JPEG image. An anchor element is then assigned this
     *  image data as its href attribute. The .jpeg file is then downloaded
     *  through a simulated click event trigger
     *  the download.
     *
     *  Arguments:
     *  - elementID = must correspond to the name of the canvas element to download from the webpage
     *
     *  */
    var canvas = document.getElementById(elementID)
    if (!canvas) {
        alert("ATTENTION: No plot has been found!");
        return;
    }

    var image = canvas.toDataURL("image/jpeg");
    var imageLink = document.createElement("a");
    imageLink.href = image;
    imageLink.download = `${elementID}_data.jpeg`;
    imageLink.click()
}

function downloadClassificationJSON(elementID) {

    /**
     * The downloadClassificationJSON function retrieves classification scores from the 'makeGraph'
     * script element and saves them as a JSON file. If no scores are available, an
     * alert notifies the user, and the function terminates.
     * The function extracts the scores using getAttribute and attempts to parse them as JSON.
     * The parsed content is stored inside a data object with a timestamp. The data is then
     * formatted using JSON.stringify for better readability.
     * A Blob object is created from the JSON data and linked to an anchor element. And then
     * a simulated cklick downloads the element.
     *
     * Arguments:
     * - elementID: The identifier used in the downloaded filename.
     */
    var scripts = document.getElementById('makeGraph');
    var classification_scores = scripts.getAttribute('classification_scores');
    if (!classification_scores) {
        alert("ATTENTION: No graph data available!");
        return;
    }
    var items = JSON.parse(classification_scores)
    var data = {scores: items, date: Date.now()};
    const jsonData = JSON.stringify(data, null);
    const blob = new Blob([jsonData], {type: "application/json"});

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${elementID}_data.json`;
    a.click();
}

function downloadHistogramJSON() {
    /**
     * The downloadHistogramJSON function generates and downloads a JSON file containing
     * the histogram data for a histogram. It retrieves data from the
     * computeHistogram function, which analyzes pixel intensities in the red, green,
     * and blue channels. If no histogram data is available, an alert notifies the user,
     * and the function terminates without proceeding.
     * Otherwise, the function structures the histogram data into a well-formatted JSON object.
     * The JSON content is then converted into a Blob object and assigned to a temporary
     * anchor element. A simulated click on the anchor then triggers the download.
     */

    const histogramData = computeHistogram();

    if (!histogramData) {
        alert("No histogram data available. Please select an image first.");
        return;
    }

    const jsonContent = `{
    "red": ${JSON.stringify(histogramData.red)},
    "green": ${JSON.stringify(histogramData.green)},
    "blue": ${JSON.stringify(histogramData.blue)}
}`;

    const blob = new Blob([jsonContent], {type: "application/json"});
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "histogram_data.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
