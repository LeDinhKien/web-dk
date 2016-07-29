/* Set height of item */
function equalHeight(group) {
    tallest = 0;
    group.each(function () {
        thisHeight = $(this).height();
        if (thisHeight > tallest) {
            tallest = thisHeight;
        }
    });
    group.each(function () {
        $(this).height(tallest);
    });
}

/* Set the height of item to match the highest height */
$(document).ready(function () {
    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    if (w > 768) {
        equalHeight($(".thumbnail"));
    }
});

