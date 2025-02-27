function syncSliderAndNumber(sliderId, inputId) {
    /**
     *  The syncSliderAndNumber function synchronizes the values between
     *  the HTML range input slider and a number input field. When a user changes
     *  the slider, the number field updates accordingly, and vice versa.
     *  The function also enforces a valid range (-100 to 100) for the number input.
     *
     *  Arguments:
     *  - sliderId = Must be the name assigned to the input range of the selected parameter in editor_select.html.
     *  - inputId  = Must be the name assigned to the input number of the selected parameter in editor_select.html.
     */

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
