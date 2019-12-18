// Update focus state of question groups
$('.qGrp input, .qGrp textarea, .qGrp select').focus(e => {
    $('.qGrp.active').removeClass('active');
    $(e.target)
        .closest('.qGrp')
        .addClass('active');
});

// Display schools from search result
$('#find-schools').click(() => displaySchools());

// Display fields based on education
$('input[name="ed"]').change(() => {
    if (
        $('input[name="ed"]:checked').val() == 'high school' ||
        $('input[name="ed"]:checked').val() == 'middle school'
    ) {
        $('#school').addClass('required');
        $('#school').removeClass('hidden');
    } else {
        $('#school').removeClass('required');
        $('#school').addClass('hidden');
    }

    if ($('input[name="ed"]:checked').val() == 'high school') {
        $('#grade').addClass('required');
        $('#grade').removeClass('hidden');
        $('#not-highschool').addClass('hidden');
    } else {
        $('#grade').removeClass('required');
        $('#grade').addClass('hidden');
        $('#not-highschool').removeClass('hidden');
    }
});

// Display guardian info fields based on age
$('#en-age').on('input change', () => {
    var age = parseInt($('#en-age').val());

    if (age >= 18) {
        $('#guardian-info .qGrp').removeClass('required');
        $('#guardian-info .qGrp').addClass('hidden');
    } else {
        $('#guardian-info .qGrp').addClass('required');
        $('#guardian-info .qGrp').removeClass('hidden');
    }
});

// Verfiy Email
$('input.email').on('input change', e => {
    var email = $(e.target).val();
    var result = /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
        email
    );
    if (email != '' && !result) {
        $(e.target).addClass('invalid');
    } else {
        $(e.target).removeClass('invalid');
    }
});

// Very Phone Number
$('input[data-mask="phone-us"]').on('input change', e => {
    var number = $(e.target).val();
    if (number) $(e.target).setMask('phone-us');
    if (number != '' && number.length != 14) {
        $(e.target).addClass('invalid');
    } else {
        $(e.target).removeClass('invalid');
    }
});

// Verify Linkedin URL
$('input#en-linkedin').on('input change', e => {
    var url = $(e.target).val();
    var result = /linkedin.com\/in\/[a-zA-Z0-9_-]+$/.test(url);
    if (url != '' && !result) {
        $(e.target).addClass('invalid');
    } else {
        $(e.target).removeClass('invalid');
    }
});

// Verify Github Username
$('input#en-github').on('input change', e => {
    var username = $(e.target).val();
    var result = /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i.test(username);
    if (username != '' && !result) {
        $(e.target).addClass('invalid');
    } else {
        $(e.target).removeClass('invalid');
    }
});

// Select school from list
$(document).on('click', '#school-list li', e => {
    $(e.target)
        .closest('li')
        .clone()
        .addClass('selected-school')
        .insertBefore('#en-school-name');
    // $('.selected-school ~ *').fadeOut(1000);
    $('.selected-school ~ *').hide();
    $(`
    <a class='button change-school'>Change School</a>
    `).appendTo('.selected-school');

    // Additional check for adding schools
    var $page = $('#basic-info');
    if (checkFilled($page)) {
        $page.find('.page-footer > .next').removeClass('disabled');
    } else {
        $page.find('.page-footer > .next').addClass('disabled');
    }
});

// Change school
$(document).on('click', '.selected-school > .change-school', () => {
    // $('.selected-school ~ *').fadeIn(1000);
    $('.selected-school ~ *').show();
    $('.selected-school').remove();
    // $('.selected-school').animate({ height: 'toggle' }, 500, () => {
    //     $('.selected-school').remove();
    // });
});

// Verify all fields
$('.page .qGrp *, #school-list li, .change-school, .progress, .page-footer').on(
    'input change click',
    e => {
        // Scan page for required fields
        var $page = $(e.target).closest('.page');

        if (checkFilled($page)) {
            $page.find('.page-footer > .next').removeClass('disabled');
            $(
                `.progress-step[data-page="#${$page.attr('id')}"] + a`
            ).removeClass('disabled');
        } else {
            $page.find('.page-footer > .next').addClass('disabled');
            $(`.progress-step[data-page="#${$page.attr('id')}"] ~ a`).addClass(
                'disabled'
            );
        }

        // Update confirmation panel
        var fields = getFields();
        $('#review-fields > table').empty();
        fields.forEach(field => {
            $(`
        <tr class="review-field">
          <td class="name">${field.name}</td>
          <td class="value">${field.displayValue}</td>
        </tr>
        `).appendTo('#review-fields > table');
        });
    }
);

// Moves to the next page
// TODO: Change page state to active.
$(document).on('click', '.page-footer > .button:not(.disabled)', e => {
    $(e.target)
        .closest('.page')
        .fadeOut(1000)
        .removeClass('active')
        .promise()
        .done(() => {
            $('.info-fields > .container').scrollTop(0);
            if (e.target.classList.contains('next')) {
                $(e.target)
                    .closest('.page')
                    .next()
                    .fadeIn(1000)
                    .addClass('active');
            } else {
                $(e.target)
                    .closest('.page')
                    .prev()
                    .fadeIn(1000)
                    .addClass('active');
            }
        });
});

// Moves to the page on the progress step
$(document).on('click', '.progress-step:not(.disabled)', e => {
    var page = $(e.target)
        .closest('.progress-step')
        .attr('data-page');

    if (`#${$('.page.active').attr('id')}` == page) return;

    $('.page.active')
        .removeClass('active')
        .fadeOut(1000)
        .promise()
        .done(() => {
            $(page)
                .fadeIn(1000)
                .addClass('active');
        });
});

$('#submit').click(() => {
    $('.page.active')
        .fadeOut(500)
        .promise()
        .done(() => {
            $('section.info-fields').css({ 'flex-basis': '0' });
            $('.progress')
                .fadeOut(1000)
                .promise()
                .done(() => {
                    // Mobile adaptation
                    $('.info-fields').hide();
                    $('.bdg').css({ height: '100%' });
                    $('.bdg > .container').show();
                    $('#attendee-reg').attr(
                        'style',
                        'margin-bottom: unset !important; height: 85vh !important'
                    );
                });
            $('.bdg .info > h1')
                .fadeOut(1000)
                .promise()
                .done(() => {
                    $('.bdg .info > h1').text('Congratulations!');
                    $('.bdg .info > h1').fadeIn(1000);
                    $('.bdg .info > .finish-msg').fadeIn(1000);
                });
        });
    // $('#attendee-reg > section:not(#complete)')
    //     .fadeOut(1000)
    //     .promise()
    //     .done(() => {
    //         $('#complete').fadeIn(1000);
    //     });
});

// Check if all required fields on the page has been filled
function checkFilled($page) {
    var filledAll = true;

    $page.find('.required').each((i, e) => {
        // Special case for school input
        if ($(e).attr('id') == 'school') {
            filledAll =
                filledAll &&
                ($('#en-school-name').val() != '' ||
                    $('.selected-school').length != 0);
            return;
        }

        var $input = $(e).find('input');
        if (
            $input.attr('type') == 'radio' ||
            $input.attr('type') == 'checkbox'
        ) {
            filledAll = filledAll && $input.is(':checked');
        } else {
            filledAll = filledAll && $input.val() && $input.val() != '';
        }
    });

    // Validate all fields
    filledAll = filledAll && $page.find('.invalid').length == 0;

    if ($page.attr('id') == 'review')
        filledAll =
            filledAll && $('#agreement .radio > input:checked').length == 3;

    return filledAll;
}

function getFields() {
    var fields = [];
    $('.page .qGrp:not(#agreement):not(#confirm)')
        .not('.hidden')
        .each((i, e) => {
            if ($(e).attr('id') == 'school') {
                if ($('.selected-school').length == 0) {
                    fields.push({
                        id: $(e).attr('id'),
                        name: 'School',
                        displayValue: $('#en-school-name').val(),
                        value: `${$('#en-school-name').val()} (${$(
                            '#en-school-zip'
                        ).val()})`,
                    });
                } else {
                    fields.push({
                        id: $(e).attr('id'),
                        name: 'School',
                        displayValue: $(
                            '.selected-school > .school-name'
                        ).text(),
                        value: `${$(
                            '.selected-school > .school-name'
                        ).text()} (${$('.selected-school > .address').text()})`,
                    });
                }
                return;
            }

            var $input = $(e).find('input, textarea');
            var name = $(e)
                .find('h3')
                .text();
            var value = $input.val();

            if ($input.attr('type') == 'radio') {
                fields.push({
                    id: $(e).attr('id'),
                    name: name,
                    displayValue: $(e)
                        .find('input:checked + span')
                        .text(),
                    value: $(e)
                        .find('input:checked')
                        .val(),
                });
            } else if ($input.attr('type') == 'checkbox') {
                fields.push({
                    id: $(e).attr('id'),
                    name: name,
                    displayValue: $(e)
                        .find('input:checked + span')
                        .map((index, elem) => {
                            return $(elem).text();
                        })
                        .get(),
                    value: $(e)
                        .find('input:checked')
                        .map((index, elem) => {
                            return $(elem).val();
                        }),
                });
            } else {
                fields.push({
                    id: $(e).attr('id'),
                    name: name,
                    displayValue: value,
                    value: value,
                });
            }
        });
    return fields;
}

// Get schools from National Center for Education Statistics (NCES)
function getSchools(params) {
    var promise = new Promise(resolve => {
        $.get(
            `./fetch_school.php?state=${
                params.state ? params.state : ''
            }&city=${params.city ? params.city : ''}&zipcode=${
                params.zipcode ? params.zipcode : ''
            }&name=${params.name ? params.name : ''}`,
            response => {
                var schools = [];
                var rows = $(response)
                    .find('table:eq(11), table:eq(15)')
                    .find('tr');

                rows.each((i, e) => {
                    let desc = $(e).find('.InstDesc');
                    let detail = $(e).find('.InstDetail');

                    if (
                        parseInt(detail.find('strong:nth-child(2)').text()) <=
                        12
                    ) {
                        schools.push({
                            name: desc.find('a').text(),
                            address: desc.html().split('<br>')[1],
                        });
                    }
                });

                resolve(schools);
            }
        );
    });
    return promise;
}

// Display search results from NCES
function displaySchools() {
    $('#school-list > .loader').css({ display: 'flex' });
    $('.no-school').hide();

    getSchools({
        state: $('#en-school-state').val(),
        city: $('#en-school-city').val(),
        zipcode: $('#en-school-zip').val(),
        name: $('#en-school-name').val(),
    }).then(response => {
        $('#school-list > ul').empty();

        var html = response
            .map(
                school => `
          <li>
            <h4 class="school-name">${school.name}</h4>
            <small class="address">${school.address}</small>
          </li>
        `
            )
            .join('');

        $('#school-list > .loader').hide();
        $('.no-school').show();
        $(html).appendTo('#school-list > ul');
    });
}

function registerAttendee() {
    var promise = new Promise((resolve, reject) => {
        var data = {};

        $('[data-field]').each((i, e) => {
            var $input = $(e);
            var name = $(e).attr('data-field');
            var value = $input.val();

            // Special cases
            // School
            if (name == 'school') {
                if ($('.selected-school').length == 0) {
                    value = $('#en-school-name').val();
                    if ($('#en-school-city').val().length != 0)
                        value += `, ${$('#en-school-city').val()}`;
                    if ($('#en-school-state').val().length != 0)
                        value += `, ${$('#en-school-state').val()}`;
                    if ($('#en-school-zip').val().length != 0)
                        value += `, ${$('#en-school-zip').val()}`;
                } else {
                    value = `${$('.selected-school .school-name').text()}, ${$(
                        '.selected-school .address'
                    ).text()}`;
                }
            }

            // Radio Buttons
            if ($input.hasClass('radio')) {
                let inpName = $input.find('input').attr('name');

                if (name == 'ethnicity') {
                    value = [];
                    $(`input[name=${inpName}]`).each((_, elem) => {
                        if ($(elem).is(':checked')) {
                            if ($(elem).is('[value=other]')) {
                                value.push(
                                    'Other: ' +
                                        $(elem)
                                            .next()
                                            .find('input')
                                            .val()
                                );
                            } else {
                                value.push($(elem).val());
                            }
                        }
                    });
                } else {
                    value = $(`input[name=${inpName}]:checked`).val();
                }
            }

            // Integers
            if (
                name == 'age' ||
                name == 'grade' ||
                name == 'previous_hackathons'
            ) {
                value = parseInt(value);
            }

            data[name] = value;
        });

        console.log(data);
        resolve(data);

        // $.post('http://localhost:8000/attendees/', JSON.stringify(data))
        //     .done(response => {
        //         resolve(response);
        //     })
        //     .fail(error => {
        //         reject(error);
        //     });
    });
    return promise;
}
