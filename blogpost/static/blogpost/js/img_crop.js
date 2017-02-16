/**
 * Created by sotnyk on 13/02/17.
 */
$(document).ready(function(){
    var img = document.getElementsByClassName('image-container');
    var width = img.clientWidth;
    var height = img.clientHeight;
    if (width > height) {
        //$('.image-container').css('height','300');
        //$('.image-container').css('width','300');
        $('.image-container').css({
            left: 0 - (width / 2),
            top: 0 - (height / 2)
        });
    }
    else if (width < height){
        //$('.image-container').css('width','300');
        $('.image-container').css({
            left: 0 - (width / 2),
            top: 0 - (height / 2)
        });
    }
});