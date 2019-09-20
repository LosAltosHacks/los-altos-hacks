/*eslint-env jquery*/
/*eslint-disable no-useless-escape*/
var lah_api = 'https://api.losaltoshacks.com';
$('.nav-link a').on('click', function(event) {
    var target = $(this.getAttribute('href'));
    if (target.length) {
        event.preventDefault();
        $('html, body')
            .stop()
            .animate(
                {
                    scrollTop: target.offset().top,
                },
                1000
            );
    }
});
$('details').attr('ontoggle', 'animateOpen(this)');
// Used in string, so eslint can't see that it's used
/* eslint-disable-next-line */
function animateOpen(ele) {
    if ($(ele).is('[open]')) {
        setTimeout(function() {
            var preh = $(ele).outerHeight();
            $(ele).css('height', preh + 'px');
        }, 520);
    } else {
        $(ele).removeAttr('style');
    }
}
$('.lah-input-group .inpctrl').keydown(function(e) {
    if (e.which == 13) {
        e.preventDefault();
        $(this).blur();
        $('.reg-button', $(this).closest('.lah-input-group')).click();
    }
});
$('.lah-input-group .reg-button').click(function() {
    if ($(this).prop('disabled')) return;
    var $parentInp = $(this).closest('.lah-input-group');
    var $input = $('input', $parentInp);
    var $btn = $(this);
    var value = $input.val();
    //input sanitation
    value = value.trim();
    var regexSafe = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
        value
    );
    if (value == '' || value == null || !regexSafe) {
        $parentInp.addClass('error');
        setTimeout(function() {
            $parentInp.removeClass('error');
        }, 1200);
        $input.focus();
        return;
    }
    $parentInp.addClass('load');
    $btn.prop('disabled', true);
    $.post(lah_api + '/email_list/v1/subscribe', { email: value })
        .done(function() {
            $parentInp.addClass('closed').removeClass('load');
            $btn.text('Registration completed.');
        })
        .fail(function(_msg) {
            $parentInp.addClass('error').removeClass('load');
            setTimeout(function() {
                $parentInp.removeClass('error');
            }, 1200);
            $input.focus();
            $btn.prop('disabled', false);
        });
});
$('.footer-icon > img').click(function() {
    $('html, body').animate({ scrollTop: 0 }, 'slow');
});

$(document).ready(function() {
    $('#view-photos').click(function(e) {
        e.preventDefault();
        $('#photo-modal').fadeIn(500);
    });

    $('#photo-modal a, #close-photo-modal').click(function() {
        $('#photo-modal').fadeOut(500);
    });
});
