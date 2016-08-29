function getCookie(name) {
    return Cookies.get(name);
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}


$(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var form_lock = false;


    $('.perpage').change(function () {
        Cookies.set('pager', $(this).val());
        window.location.reload();
    });

    var collids = function () {
        var lc = [];

        $('.courses-list').each(function () {
            if (typeof $(this).data('id') !== 'undefined') {
                lc.push($(this).data('id'));
            }
        });

        $('input.courses').val(lc.join(','));
    };

    $('.courses-block button').click(function () {
        var $t = $('select.courses');
        var opt = $t.find('option[value="' + $t.val() + '"]');
        var text = opt.text();
        var atrv = opt.attr('value');

        $('<div data-id="' + atrv + '" data-name="' + text + '" class="courses-list">' + text + '<span class="cross">x</span></div>').insertAfter('input.courses');

        collids();

        opt.remove();

        if ($('select.courses').find('option').length > 0) {
            $('.courses-block').show();
        } else {
            $('.courses-block').hide();
        }
        return false;
    });

    $(document).on('click', '.cross', function () {
        var $t = $(this).parent();

        var id = $t.data('id');
        var val = $t.data('name');

        $('select.courses').append('<option value="' + id + '">' + val + '</option>');

        $t.remove();

        collids();

        if ($('select.courses').find('option').length > 0) {
            $('.courses-block').show();
        } else {
            $('.courses-block').hide();
        }
    });

    var vals = $('input.courses').val();
    if (typeof vals !== 'undefined') {
        $.each(vals.split(','), function (k, v) {
            if (v) {
                $('select.courses').val(v);
                $('.courses-block button').click();
            }
        });
    }


    $('.userform form').submit(function (e) {
        e.preventDefault();
        e.stopPropagation();

        if (form_lock) {
            return false;
        }

        var $t = $(this);

        $.ajax(window.location.href, {
            method: 'post',
            type: 'json',
            data: $t.serialize(),
        }).done(function (data) {
            if (data.status) {
                $('.notify-ok').show('slow');
                form_lock = true;

                setTimeout(function () {
                    window.location.href = '/';
                }, 3000);
            } else {
                $('.ins-error').remove();
                for (var k in data.errors) {
                    $('<div class="ins-error"></div>').insertAfter($t.find('input[name=' + k + ']')).html(data.errors[k]);
                }
            }
        }).fail(function () {
            alert("Sorry, an error happened");
        });
        return false;
    });
});