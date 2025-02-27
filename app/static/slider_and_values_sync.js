//  a simple javascript function used to sync both sliders and numbers input

function syncSliderAndNumber(sliderId, inputId) {
    let slider = document.getElementById(sliderId);
    let input = document.getElementById(inputId);

    slider.addEventListener('input', function () {
        input.value = this.value;
    });

    input.addEventListener('input', function () {
        if (this.value < -100) this.value = -100;
        if (this.value > 100) this.value = 100;
        slider.value = this.value;
    });
}

syncSliderAndNumber('colorRange', 'colorValue');
syncSliderAndNumber('brightnessRange', 'brightnessValue');
syncSliderAndNumber('contrastRange', 'contrastValue');
syncSliderAndNumber('sharpnessRange', 'sharpnessValue');
