/* Enable text input (Sale) */
document.getElementById('Box').onchange = function () {
    document.getElementById('sale').disabled = !this.checked;
};

/* Show tooltip */
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

/* Validate form */
function validateForm() {
    if (!document.getElementById("sale").disabled) {
        // Get the value of the input field with id="sale"
        var x = document.getElementById("sale").value;

        // If x is Not a Number or less than zero or greater than 100
        if (isNaN(x) || x < 0 || x > 100) {
            alert("Input not valid");
            return false;
        }
    }

    var name = document.forms["myForm"]["name"].value;
    if (name == null || name == "") {
        alert("Product name must be filled out");
        return false;
    }

    var price = document.forms["myForm"]["price"].value;
    if (name == null || name == "") {
        alert("Product price must be filled out");
        return false;
    }
}
