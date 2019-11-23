var school;

$('.qGrp input, .qGrp textarea, .qGrp select').focus(e => {
    $('.qGrp.active').removeClass('active');
    $(e.target)
        .closest('.qGrp')
        .addClass('active');
});

$('#find-schools').click(e => displaySchools(e));

$('input[name="ed"]').change(e => {
    if (
        $('input[name="ed"]:checked').val() == 'high school' ||
        $('input[name="ed"]:checked').val() == 'middle school'
    ) {
        $('#school').show();
    } else {
        $('#school').hide();
    }

    if ($('input[name="ed"]:checked').val() == 'high school') {
        $('#grade').show();
        $('#not-highschool').hide();
    } else {
        $('#grade').hide();
        $('#not-highschool').show();
    }
});

$(document).on('click', '#school-list li', e => {
    $(e.target)
        .closest('li')
        .clone()
        .addClass('selected-school')
        .insertBefore('#en-school-name');
    $('.selected-school ~ *').fadeOut(1000);
    $(`
    <a class='button change-school'>Change School</a>
    `).appendTo('.selected-school');
});

$(document).on('click', '.selected-school > .change-school', e => {
    $('.selected-school ~ *').fadeIn(1000);
    $('.selected-school').animate({ height: 'toggle' }, 500, () => {
        $('.selected-school').remove();
    });
});

// TODO: Change page state to active.
$('.page-footer > .button:not(.disabled)').click(e => {
    $(e.target)
        .closest('.page')
        .fadeOut(1000)
        .promise()
        .done(() => {
            if (e.target.classList.contains('next')) {
                $(e.target)
                    .closest('.page')
                    .next()
                    .fadeIn(1000);
            } else {
                $(e.target)
                    .closest('.page')
                    .prev()
                    .fadeIn(1000);
            }
        });
});

function getSchools(params) {
    var promise = new Promise((resolve, reject) => {
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

function displaySchools(e) {
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
