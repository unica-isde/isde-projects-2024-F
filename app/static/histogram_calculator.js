function displayImage() {
    /**
     * The displayImage function is responsible for updating an image on
     * the histogram computation section of the webpage.
     * It retrieves the selected image filename from the imageSelector
     * dropdown menu, constructs the corresponding file path,
     * and updates the src attribute of an image element.
     * It also manages the visibility of UI sections by modifying the webpage
     * after the image submission and triggers the histogram
     * computation upon successful image loading.
     */
    const imageSelector = document.getElementById("imageSelector");
    const selectedImage = imageSelector.value;

    const imagePath = `/static/imagenet_subset/${selectedImage}`;
    const imageElement = document.getElementById("selectedImage");
    imageElement.src = imagePath;

    document.getElementById("infoSection").style.display = "none";
    document.getElementById("imageHistogramSection").style.display = "block";

    imageElement.onload = function () {
        const histogramData = computeHistogram();
        if (histogramData) {
            plotHistogram(histogramData.red, histogramData.green, histogramData.blue);
        }
    };

    imageElement.onerror = function () {
        console.error("Image not found at: ", imagePath);
        alert("Error: Image not found! Check filename or static folder.");
    };
}

function computeHistogram() {
    /**
     * The computeHistogram function analyzes the pixel data of a selected image
     * and calculates the histogram distribution for the red, green, and blue
     * color channels. It extracts pixel intensity values from the image, processes the RGB
     * components, and counts the frequency of each intensity level for
     * each color channel.
     *
     * The function then returns three arrays of 256 elements:
     *  -  red[]   : Distribution of red intensity values.
     *  -  green[] : Distribution of green intensity values.
     *  -  blue[]  : Distribution of blue intensity values.
     *
     * These arrays can be used for further data manipulation, visualization,
     * or exporting histogram data.
     */
    const imageElement = document.getElementById("selectedImage");

    if (!imageElement || !imageElement.src) {
        console.error("No image loaded.");
        return null;
    }

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = imageElement.width;
    canvas.height = imageElement.height;
    ctx.drawImage(imageElement, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    let red = new Array(256).fill(0);
    let green = new Array(256).fill(0);
    let blue = new Array(256).fill(0);

    for (let i = 0; i < data.length; i += 4) {
        red[data[i]]++;
        green[data[i + 1]]++;
        blue[data[i + 2]]++;
    }

    return {red, green, blue};
}

let histogramChart = null;

function plotHistogram(red, green, blue) {
    /**
     * The plotHistogram function receives the RGB data extracted by computeHistogram
     * and plots the histogram using canvas.
     *
     * Arguments:
     *  - red   = Must be the red distribution array calculated by the computeHistogram function.
     *  - green = Must be the green distribution array calculated by the computeHistogram function.
     *  - blue  = Must be the blue distribution array calculated by the computeHistogram function.
     */
    const canvasElement = document.getElementById("histogram_output");

    if (!canvasElement) {
        console.error("Canvas element not found.");
        return;
    }

    const ctx = canvasElement.getContext("2d");

    if (histogramChart !== null) {
        histogramChart.destroy();
    }


    histogramChart = new Chart(ctx, {
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