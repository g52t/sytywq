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

function getImageSrc(el) {
    return el.src || $(el).attr('data-original')
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
    $('img').click(function (el) {
        let src = getImageSrc(this);
        console.log(src);
        if (WeixinJSBridge) {
            let imgs = [];
            $.each($('img'), function (i, im) {
                let s = getImageSrc(im);
                if (s) {
                    imgs.push(s);
                }
            });
            WeixinJSBridge.invoke("imagePreview", {
                "urls": imgs,
                "current": src
            });
        } else {
            window.open(src);
        }
    });
});