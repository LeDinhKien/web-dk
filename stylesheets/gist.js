$('ul.nav li.dropdown').hover(function () {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
}, function () {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
});

// function validateForm() {
//     var x = document.forms["myForm"]["name"].value;
//     if (x == null || x == "") {
//         alert("Product name must be filled out");
//         return false;
//     }
// }

//        function addForm() //}
//            $form = $("<form></form>");
//            $form.append('<div class="input-group input-group-lg">' +
//                    '<span class="input-group-addon">Category</span>' +
//                    '<input type="text" name="category" class="form-control" value="category_name">' +
//                    '<span class="input-group-btn"> ' +
//                    '<button class="btn btn-default" type="submit">Save</button></span>' +
//                    '</div>');
//            $form.append('<input type="button" value="BUTTON">');
//            $('#forForm').append($form);
//        }