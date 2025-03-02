function buildFancybox() {
    $(".article-container section img").unwrap();
    let images = Array.from($('.article-container section img'));
    if (!images.length) return;

    images.forEach(el => {
        const src = $(el).attr("src");
        const alt = $(el).attr("alt") || '';
        $(el).after(`<a href="${src}" data-download-src="${src}" data-caption="${alt}" data-fancybox="gallery"><img src="${src}"/></a>`);
        $(el).remove();
    });

    window.Fancybox.bind('[data-fancybox="gallery"]', {
        Toolbar: {
            display: [
                "counter",
                "zoom",
                "slideshow",
                "fullscreen",
                "download",
                "thumbs",
                "close",
            ],
        },
        Image: {
            zoom: false,
        },
        showClass: "fancybox-zoomIn",
        hideClass: "fancybox-zoomOut",
    });

}


buildFancybox();