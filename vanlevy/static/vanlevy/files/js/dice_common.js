function switchAndCollapse (button, buttons, div, divs, Normal, Deactivated){
    $(button).removeClass(Normal).addClass(Deactivated);
    $(button).prop("disabled", true);
    for (var element of buttons){
        $(element).prop("disabled", false);
        $(element).removeClass(Deactivated).addClass(Normal);
    };
    $(div).collapse("show");
    for (var unit of divs) {
        $(unit).collapse("hide");
    };
};

function collapseCard (collapse, card, switchClass, button, otherButton) {
    $(collapse).collapse("hide");
    $(card).removeClass(switchClass);
    $(otherButton).css("display", "inline");
    $(button).css("display", "none");
};

function showCard (collapse, card, switchClass, button, otherButton) {
    $(collapse).collapse("show");
    $(card).addClass(switchClass);
    $(otherButton).css("display", "inline");
    $(button).css("display", "none");
};
