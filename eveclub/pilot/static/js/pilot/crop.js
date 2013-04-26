$(function() {
    $('#cropbox').Jcrop({
        aspectRatio: 1,
        onSelect: updateCoords,
        minSize: [128, 128]
    });
});

function updateCoords(c) {
    $('#x').val(c.x);
    $('#y').val(c.y);
    $('#w').val(c.w);
    $('#h').val(c.h);
};

function checkCoords() {
    if (parseInt($('#w').val())) return true;
    alert('Please select a crop region then press submit.');
    return false;
};