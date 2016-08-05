/* 
 * Javascript for add/edit product pages
 * */

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
            alert("Sale percentage is not valid");
            return false;
        }
    }

    var name = document.forms["myForm"]["name"].value;
    if (!name) {
        alert("Product name must be filled out");
        return false;
    }

    var price = document.forms["myForm"]["price"].value;
    if (!price) {
        alert("Product price must be filled out");
        return false;
    }

    var category = document.forms["myForm"]["category"].value;
    if (!category) {
        alert("You must add a category first");
        return false;
    }
}

/* Remove images URL field */
function remove_field(element) {
    element.parentNode.parentNode.remove();
}

/* Add images URL field */
$("#add-field").click(function () {
    $("#extra-url").append('<div class="input-group add-space">' +
        '<input type="text" class="form-control" name="pic_url" placeholder="URL">' +
        '<span class="input-group-btn">' +
        '<button class="btn btn-secondary" type="button" onclick="remove_field(this)">&times;</button>' +
        '</span>' +
        '</div>');
});
