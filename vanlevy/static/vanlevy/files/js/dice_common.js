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


// dice room info pages
function switchDisplays (blockIDs, noneIDs) {
    for (var element of blockIDs){
        $(element).css("display", "block");
    };
    for (var unit of noneIDs){
        $(unit).css("display", "none");
    };
}
function switchButtonsToggleDiv (buttonOne, buttonTwo, div){
    $(buttonOne).css("display", "none");
    $(buttonTwo).css("display", "inline");
    $(div).collapse("toggle");
};
function fourButtonTwoCollapse (buttonOne, buttonTwo, buttonThree, buttonFour, divOne, divTwo){
    $(buttonOne).css("display", "none");
    $(buttonTwo).css("display", "inline");
    $(buttonThree).css("display", "inline");
    $(buttonFour).css("display", "none");
    $(divOne).collapse("show");
    $(divTwo).collapse("hide");
};
function switchButtonHideDiv (buttonOne, buttonTwo, div) {
    $(buttonOne).css("display", "none");
    $(buttonTwo).css("display", "inline");
    $(div).collapse("hide");
};


//common to dice room info pages and hub rooms
function copyTextToClipboard(text) {
  var textArea = document.createElement("textarea");

  // Place in top-left corner of screen regardless of scroll position.
  textArea.style.position = 'fixed';
  textArea.style.top = 0;
  textArea.style.left = 0;

  // Ensure it has a small width & height. Setting to 1px / 1em doesn't work as this gives a negative w/h on some browsers.
  textArea.style.width = '2em';
  textArea.style.height = '2em';

  // We don't need padding, reducing the size if it does flash render.
  textArea.style.padding = 0;

  // Clean up any borders.
  textArea.style.border = 'none';
  textArea.style.outline = 'none';
  textArea.style.boxShadow = 'none';

  // Avoid flash of white box if rendered for any reason.
  textArea.style.background = 'transparent';

  textArea.value = text;

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Copying text command was ' + msg);
  } catch (err) {
    console.log('Oops, unable to copy');
  }

  document.body.removeChild(textArea);
}

function copyURL(element){
    console.log(element.innerText);
    var copyText = element.innerText;
    copyTextToClipboard(copyText)
    var msg = (copyText).concat(" copied to clipboard.")
    alert(msg);
}

// Player-Info Page
function showMakeGM() {
    document.getElementById('make_gm').style.display='none';
    document.getElementById('cancel_make_gm').style.display='block';
    document.getElementById('gm_instructions').style.display='none';
    document.getElementById('gm_transfer').style.display='block';
    document.getElementById('ban_button').style.display='none';
}
function hideMakeGM() {
    document.getElementById('make_gm').style.display='block';
    document.getElementById('cancel_make_gm').style.display='none';
    document.getElementById('gm_instructions').style.display='block';
    document.getElementById('gm_transfer').style.display='none';
    document.getElementById('ban_button').style.display='block';
}
function showBan() {
    document.getElementById('ban').style.display='none';
    document.getElementById('cancel_ban').style.display='block';
    document.getElementById('gm_instructions').style.display='none';
    document.getElementById('ban_area').style.display='block';
    document.getElementById('gm_button').style.display='none';
}
function hideBan() {
    document.getElementById('ban').style.display='block';
    document.getElementById('cancel_ban').style.display='none';
    document.getElementById('gm_instructions').style.display='block';
    document.getElementById('ban_area').style.display='none';
    document.getElementById('gm_button').style.display='block';
}
function showUnban() {
    document.getElementById('unban').style.display='none';
    document.getElementById('cancel_unban').style.display='block';
    document.getElementById('gm_instructions').style.display='none';
    document.getElementById('ban_area').style.display='block';
}
function hideUnban() {
    document.getElementById('unban').style.display='block';
    document.getElementById('cancel_unban').style.display='none';
    document.getElementById('gm_instructions').style.display='block';
    document.getElementById('ban_area').style.display='none';
}