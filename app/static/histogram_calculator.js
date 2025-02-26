function displayImage() {

    const imageSelector = document.getElementById("imageSelector");
    const selectedImage = imageSelector.value;

    const imagePath = `/static/imagenet_subset/${selectedImage}`;
    console.log("Loading image from:", imagePath);

    const imageElement = document.getElementById("selectedImage");
    imageElement.src = imagePath;

    document.getElementById("infoSection").style.display = "none";
    document.getElementById("imageHistogramSection").style.display = "block";

    imageElement.onload = function () {
        console.log("Image loaded successfully.");
        computeHistogram();
    };


    imageElement.onerror = function () {
        console.error("Failed to load image at", imagePath);
        alert("Error: Image not found! Check filename or static folder.");
    };
}

function computeHistogram() {
    const imageElement = document.getElementById("selectedImage");

    if (!imageElement || !imageElement.src) {
        console.error("No image loaded.");
        return;
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

    plotHistogram(red, green, blue);
}

let histogramChart = null;

function plotHistogram(red, green, blue) {
    const canvasElement = document.getElementById("histogramOutput");

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
