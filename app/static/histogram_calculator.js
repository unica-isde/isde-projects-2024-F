$(document).ready(function () {
    var imageElement = document.getElementById("selectedImage");

    if (!imageElement || !imageElement.src) {
        console.error("No image source found at page load.");
        return;
    }

    console.log("Image Source: ", imageElement.src);

    if (imageElement.complete) {
        processHistogram();
    } else {
        imageElement.onload = processHistogram;
    }
});


function processHistogram() {
    /**
     * Process and plot the histogram for the loaded image.
     */
    var histogramData = computeHistogram();
    if (histogramData) {
        plotHistogram("histogram_output", histogramData.red, histogramData.green, histogramData.blue);
    }
}

function computeHistogram() {
    var imageElement = document.getElementById("selectedImage");

    if (!imageElement || !imageElement.src) {
        console.error("No image loaded.");
        return null;
    }

    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext("2d");

    canvas.width = imageElement.width;
    canvas.height = imageElement.height;
    ctx.drawImage(imageElement, 0, 0, canvas.width, canvas.height);
    var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    var data = imageData.data;

    var red = new Array(256).fill(0);
    var green = new Array(256).fill(0);
    var blue = new Array(256).fill(0);

    for (var i = 0; i < data.length; i += 4) {
        red[data[i]]++;
        green[data[i + 1]]++;
        blue[data[i + 2]]++;
    }

    console.log("Computed Histogram Data: ", {red, green, blue});

    return {red, green, blue};
}


function plotHistogram(canvasId, red, green, blue) {
    /**
     * Helper function to plot histogram data into a specified canvas.
     */
    var canvasElement = document.getElementById(canvasId);
    if (!canvasElement) {
        console.error(`Canvas element ${canvasId} not found.`);
        return;
    }

    var ctx = canvasElement.getContext("2d");

    if (canvasElement.histogramChart) {
        canvasElement.histogramChart.destroy();
    }

    canvasElement.histogramChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: Array.from({length: 256}, (_, i) => i),
            datasets: [
                {label: "Red", data: red, backgroundColor: "red"},
                {label: "Green", data: green, backgroundColor: "green"},
                {label: "Blue", data: blue, backgroundColor: "blue"}
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {title: {display: true, text: "Pixel Value"}},
                y: {title: {display: true, text: "Count"}}
            }
        }
    });
}
