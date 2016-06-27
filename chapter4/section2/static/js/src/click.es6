$(() => {
    let $D = $(document);
    function listener() {
        $D.on('click', '.pure-button', function() {
            $(this).css("background-color", "pink");
        });
    }

    listener();
});
