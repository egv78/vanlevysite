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
// dice rooms - common

function showSecretRoll() {
    document.getElementById('secret_warning').style.display='block';
    document.getElementById('show_secret_roll_button').style.display='none';
    document.getElementById('hide_secret_roll_button').style.display='block';
    document.getElementById('roll_dice_button').style.display='none';
    document.getElementById('roll_dice_secret_button').style.display='block';
};
function hideSecretRoll() {
    document.getElementById('secret_warning').style.display='none';
    document.getElementById('show_secret_roll_button').style.display='block';
    document.getElementById('hide_secret_roll_button').style.display='none';
    document.getElementById('roll_dice_button').style.display='block';
    document.getElementById('roll_dice_secret_button').style.display='none';
};
function addOne(id) {
    document.getElementById(id).stepUp(1);
};
function subtractOne(id) {
    document.getElementById(id).stepDown(1);
};

function highlightChat() {
  var number = document.getElementById("id_recipient").selectedIndex;
  var button = document.getElementById("chat_submit");
  var chat_area = document.getElementById("chat_text");
  if (number > 0) {
    button.classList.remove('btn-outline-dark');
    button.classList.add('btn-outline-warning');
    button.textContent = 'Whisper';
    chat_area.classList.add('chat_whisper');
    chat_area.classList.remove('chat_regular');
  } else {
    button.classList.remove('btn-outline-warning');
    button.classList.add('btn-outline-dark');
    button.textContent = 'Add Chat';
    chat_area.classList.remove('chat_whisper');
    chat_area.classList.add('chat_regular');
  };
};
function show(id) {
    document.getElementById(id).style.display='inline';
};
function hide(id) {
    document.getElementById(id).style.display='none';
};

// dice room common - page updates
$(function () {
    var dt = new Date();
    document.getElementById('updateTime').innerText = dt.toISOString();
    update_times();
});

$(function () {
  var number = document.getElementById("id_recipient").selectedIndex;
  var button = document.getElementById("chat_submit");
  var chat_area = document.getElementById("chat_text");
  if (number > 0) {
    chat_area.classList.add('chat_whisper');
    chat_area.classList.remove('chat_regular');
  };
});
var myForm = $("#destiny");
myForm.submit(function(){
    myForm.submit(function(){
        return false;
    });
});
var mySecondForm = $("#dice");
mySecondForm.submit(function(){
    mySecondForm.submit(function(){
        return false;
    });
});
var myThirdForm = $("#chat");
myThirdForm.submit(function(){
    myThirdForm.submit(function(){
        return false;
    });
});
function refresh_action_log(){
    var url_actions = document.URL + ' #action_log';
    var url_destiny = document.URL + ' #destiny_area';
    $('#action_log').load(url_actions);
    $('#destiny_area').load(url_destiny);
};
function refresh_chat_log() {
    var url_chat_log = document.URL + ' #chat_log';
    $('#chat_log').load(url_chat_log);
};
function check_and_update() {
    var pageUpdate = new Date(document.getElementById('updateTime').innerText);
    var actionUpdate = new Date($("#actionTime").text());
    var chatUpdate = new Date($("#chatTime").text());
    var now = new Date();
    if (actionUpdate > pageUpdate && chatUpdate > pageUpdate) {
        refresh_action_log();
        refresh_chat_log();
        document.getElementById('updateTime').innerText = now.toISOString();
    } else if (actionUpdate > pageUpdate) {
        refresh_action_log();
        document.getElementById('updateTime').innerText = now.toISOString();
    } else if (chatUpdate > pageUpdate) {
        refresh_chat_log();
        document.getElementById('updateTime').innerText = now.toISOString();
    };
};
function update_times() {
    var url_action_time = document.URL + ' #last_times';
    $('#last_times').load(url_action_time, function () {
        // When it loads, schedule the next request for 1s later
        setTimeout(update_times, 1000)
    });
    check_and_update();
};

// dice room - specific to rooms
function resetDiceGen() {
    document.getElementById('boost').value = 0;
    document.getElementById('setback').value = 0;
    document.getElementById('ability').value = 0;
    document.getElementById('difficulty').value = 0;
    document.getElementById('proficiency').value = 0;
    document.getElementById('challenge').value = 0;
    document.getElementById('force').value = 0;
    document.getElementById('numerical').value = 0;
    document.getElementById('sides').value = 100;
    document.getElementById('triumph').value = 0;
    document.getElementById('despair').value = 0;
    document.getElementById('success').value = 0;
    document.getElementById('failure').value = 0;
    document.getElementById('advantage').value = 0;
    document.getElementById('threat').value = 0;
    document.getElementById('lightpip').value = 0;
    document.getElementById('darkpip').value = 0;
};
function resetDiceSW() {
    document.getElementById('boost').value = 0;
    document.getElementById('setback').value = 0;
    document.getElementById('ability').value = 0;
    document.getElementById('difficulty').value = 0;
    document.getElementById('proficiency').value = 0;
    document.getElementById('challenge').value = 0;
    document.getElementById('force').value = 0;
    document.getElementById('numerical').value = 0;
    document.getElementById('sides').value = 100;
    document.getElementById('triumph').value = 0;
    document.getElementById('despair').value = 0;
    document.getElementById('success').value = 0;
    document.getElementById('failure').value = 0;
    document.getElementById('advantage').value = 0;
    document.getElementById('threat').value = 0;
    document.getElementById('lightpip').value = 0;
    document.getElementById('darkpip').value = 0;
};
function resetDiceMYZ() {
    document.getElementById('base').value = 0;
    document.getElementById('skill').value = 0;
    document.getElementById('gear').value = 0;
    document.getElementById('d6').value = 0;
    document.getElementById('d66').value = 0;
    document.getElementById('d666').value = 0;
    document.getElementById('is_pushed').checked = false;
    document.getElementById('numerical').value = 0;
    document.getElementById('sides').value = 100;
    document.getElementById('trauma').value = 0;
    document.getElementById('failure').value = 0;
    document.getElementById('damage').value = 0;
    document.getElementById('success_base').value = 0;
    document.getElementById('success_skill').value = 0;
    document.getElementById('success_gear').value = 0;
    document.getElementById('reset_dice').style.display='none';
    document.getElementById('setup_push').style.display='block';
    changeSkillImage();
};
function resetDicePoly() {
    document.getElementById('d4').value = 0;
    document.getElementById('d6').value = 0;
    document.getElementById('d8').value = 0;
    document.getElementById('d10').value = 0;
    document.getElementById('d12').value = 0;
    document.getElementById('d20').value = 0;
    document.getElementById('d100').value = 0;
    document.getElementById('numerical').value = 0;
    document.getElementById('sides').value = 999;
    document.getElementById('bonus').value = 0;
};

function showAutoPipsGenSW() {
    document.getElementById('hidden_fields_1').style.display='flex';
    document.getElementById('show_pips_button').style.display='none';
    document.getElementById('hide_pips_button').style.display='block';
};
function hideAutoPipsGenSW() {
    document.getElementById('hidden_fields_1').style.display='none';
    document.getElementById('show_pips_button').style.display='block';
    document.getElementById('hide_pips_button').style.display='none';
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