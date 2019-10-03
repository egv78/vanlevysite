function enableGravatarButtons () {
    document.getElementById('gravatar_button').disabled = false;
    document.getElementById('identicon_button').disabled = false;
    document.getElementById('monsterid_button').disabled = false;
    document.getElementById('wavatar_button').disabled = false;
    document.getElementById('retro_button').disabled = false;
    document.getElementById('robohash_button').disabled = false;
};
function useGravatar(url, button) {
    document.getElementById('image_url').value = url;
    $('#new_image').attr('src', url);
    enableGravatarButtons();
    document.getElementById(button).disabled = true;
};
function clearImageURL(noPic) {
    var old_url = noPic;
    document.getElementById('image_url').value = "";
    $('#new_image').attr('src', old_url);
};
function preview(noPic) {
    var new_url = document.getElementById('image_url').value;
    if (new_url == "") {
      new_url = noPic;
    };
    var new_first_name = document.getElementById('name').value;
    var new_description_text = document.getElementById('description').value;

    $('#new_image').attr('src', new_url);

    $('#new_name').text(new_first_name);
    $('#new_description').text(new_description_text);
};

function revertImageURL() {
  var old_url = document.getElementById('initial_url').innerText;
  document.getElementById('image_url').value = old_url;
};

function previewProfile() {
  var new_url = document.getElementById('image_url').value;
  var new_first = document.getElementById('first_name').value;
  var new_last = document.getElementById('last_name').value;
  var new_about = document.getElementById('about_me').value;
  var new_gaming = document.getElementById('gaming_interests').value;
  var new_location = document.getElementById('location').value;

  img_element = $('#new_image');
  img_element.attr('src', new_url);

  $('#new_first_name').text(new_first);
  $('#new_last_name').text(new_last);
  $('#new_about_me').text(new_about);
  $('#new_gaming_interests').text(new_gaming);
  $('#new_location').text(new_location);
};

function showWhyEmail() {
    document.getElementById('whyEmail').style.display='block';
    document.getElementById('showButton').style.display='none';
};
function hideWhyEmail() {
    document.getElementById('whyEmail').style.display='none';
    document.getElementById('showButton').style.display='inline';
};