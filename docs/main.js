function launchFullscreen(element) {
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    } else if (element.oRequestFullscreen) {
        element.oRequestFullscreen();
    }
}

function stopVideo(el) {
    $.each($("video"), function (i, v) {
        if (el !== v)
            v.pause()
    });
}

$(function () {
    $("img.lazyload").lazyload({effect: "fadeIn"});
    $.each($(".video"), function (i, v) {
        $(v).find('.btn-play').click(function () {
            let el = $(v).find('video')[0];
            stopVideo(el);
            if (el.paused) {
                el.play();
                $(el).attr('controls', 'controls');
                //launchFullscreen(el);
            } else
                el.pause();
        });
    })

});