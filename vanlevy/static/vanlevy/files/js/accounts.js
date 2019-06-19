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

function showWhyEmail() {
    document.getElementById('whyEmail').style.display='block';
    document.getElementById('showButton').style.display='none';
};
function hideWhyEmail() {
    document.getElementById('whyEmail').style.display='none';
    document.getElementById('showButton').style.display='inline';
};