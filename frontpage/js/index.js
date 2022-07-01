var eventsList = document.querySelectorAll('#schedule-table tbody > tr');
var clockTime = 0;
var events = [];

registerEvents();

// Adapt to Microsoft Edge
if (!(/*@cc_on!@*/ (false || !!document.documentMode))) {
    adaptEdge();
}

// Register all events
function registerEvents() {
    // Compile events into a list
    for (var i = 0; i < eventsList.length; i++) {
        var node = eventsList[i];

        var day = node.parentNode.parentNode.parentNode.parentNode.parentNode.classList.contains(
            'sunday'
        )
            ? 'Sunday'
            : 'Saturday';
        var time = node.querySelector('td:first-child').textContent;
        time = convertToMinutes(time, day);
        var name = node.querySelector('.event-name').textContent;
        let location = node.querySelector('.location').textContent;
        events.push({
            id: i,
            name: name,
            day: day,
            time: time,
            location: location,
        });

        if (i == 0) {
            clockTime = time;
            clockDisplayUpdate();
        }
    }

    // Register onclick listener for all events
    eventsList.forEach(node => {
        node.addEventListener('click', _ => {
            // To prevent discrepancy between rotation animation and scrolling
            document.querySelector(
                '#hour-pointer > span, #minute-pointer'
            ).style.transition = 'transform 0.5s';

            // Update clock time
            var index = Array.prototype.slice
                .call(
                    document.querySelector('#schedule-table > .saturday tbody')
                        .children
                )
                .concat(
                    Array.prototype.slice.call(
                        document.querySelector(
                            '#schedule-table > .sunday tbody'
                        ).children
                    )
                )
                .indexOf(node);
            var ev = events[index];
            var day = ev.day;
            var name = ev.name;
            var time = parseTime(ev.time);
            var location = ev.location;
            clockTime = ev.time;

            // Update clock display
            var parameters = document.querySelector('#clock > .content')
                .children;
            parameters[0].textContent = day;
            parameters[1].textContent = time;
            parameters[2].textContent = name;
            parameters[3].textContent = location;

            clockDisplayUpdate();
        });
    });

    let scheduleSwitchClosure = (() => {
        let showSunday = false;
        return _event => {
            showSunday = !showSunday;
            if (!showSunday) {
                document.querySelector(
                    '#schedule-table .sunday'
                ).style.display = 'none';
                document.querySelector(
                    '#schedule-table .saturday'
                ).style.display = 'unset';
            } else {
                document.querySelector(
                    '#schedule-table .saturday'
                ).style.display = 'none';
                document.querySelector(
                    '#schedule-table .sunday'
                ).style.display = 'unset';
            }
        };
    })();
    document
        .querySelector('#schedule-table .saturday > header')
        .addEventListener('click', scheduleSwitchClosure);
    document
        .querySelector('#schedule-table .sunday > header')
        .addEventListener('click', scheduleSwitchClosure);

    // Register scrolling listener for clock
    document.getElementById('clock').addEventListener('wheel', e => {
        // To prevent discrepancy between rotation animation and scrolling
        document.querySelector(
            '#hour-pointer > span, #minute-pointer > span'
        ).style.transition = 'none';

        if (e.deltaY == 0) return;
        clockTime += e.deltaY < 0 ? -15 : 15;

        if (clockTime <= events[0].time) {
            clockTime = events[0].time;
        }

        if (clockTime >= events[events.length - 1].time) {
            clockTime = events[events.length - 1].time;
        }

        clockDisplayUpdate();

        e.preventDefault();
    });
}

// Update clock according to clockTime
function clockDisplayUpdate() {
    var angle = clockTime / 2;
    document.querySelector(
        '#hour-pointer > span'
    ).style.transform = `rotate(${angle}deg)`;
    document.querySelector(
        '#minute-pointer > span'
    ).style.transform = `rotate(${clockTime * 6}deg)`;
    document.querySelector(
        '#clock > .content'
    ).children[1].textContent = parseTime(clockTime);

    if (clockTime >= 1440) {
        document.querySelector('#clock > .content').children[0].textContent =
            'Sunday';
        document.querySelector('#clock > .sunday').style.transform =
            'translate(-50%, -50%) scale(1)';
        document.querySelector('#clock > .saturday').style.transform =
            'translate(-50%, -50%) scale(0.9)';

        document.querySelector('#schedule-table .sunday').style.display =
            'unset';
        document.querySelector('#schedule-table .saturday').style.display =
            'none';
    } else {
        document.querySelector('#clock > .content').children[0].textContent =
            'Saturday';
        document.querySelector('#clock > .sunday').style.transform =
            'translate(-50%, -50%) scale(0.9)';
        document.querySelector('#clock > .saturday').style.transform =
            'translate(-50%, -50%) scale(1)';

        document.querySelector('#schedule-table .sunday').style.display =
            'none';
        document.querySelector('#schedule-table .saturday').style.display =
            'unset';
    }

    // Update table according to time
    eventsList.forEach(node => {
        node.classList.remove('active'); // Reset active item
    });

    for (var i = 0; i < events.length - 1; i++) {
        var parameters = document.querySelector('#clock > .content').children;
        if (events[i].time <= clockTime && events[i + 1].time > clockTime) {
            eventsList[i].classList = 'active';
            parameters[0].textContent = events[i].day;
            parameters[2].textContent = events[i].name;
            parameters[3].textContent = events[i].location;
            break;
        }
        if (clockTime == events[events.length - 1].time) {
            eventsList[events.length - 1].classList = 'active';
            parameters[0].textContent = events[events.length - 1].day;
            parameters[2].textContent = events[events.length - 1].name;
            parameters[3].textContent = events[events.length - 1].location;
            break;
        }
    }
}

// Helper Function: Returns proper string format given minutes
function parseTime(time) {
    var suffix = time < 720 || (time >= 1440 && time < 2160) ? 'AM' : 'PM';
    var hours = Math.floor(time / 60) % 12;
    if (suffix === 'PM' && hours == 0) hours = 12;
    if (hours < 10) hours = `0${hours}`;
    var minutes = Math.floor(time % 60);
    if (minutes < 10) minutes = `0${minutes}`;

    return `${hours}:${minutes} ${suffix}`;
}

// Helper Function: Returns minutes given string format of time
function convertToMinutes(time, day) {
    var parsedTime = time.match(/\d{2}/g).map(e => {
        return parseInt(e);
    });
    return (
        (parsedTime[0] % 12) * 60 +
        parsedTime[1] +
        (time.includes('PM') ? 720 : 0) +
        (day == 'Sunday' ? 1440 : 0)
    );
}

// Adapt to Microsoft Edge, which doesn't have details tag support
function adaptEdge() {
    var answers = document.querySelectorAll('.question > .answer');
    for (var i = 0; i < answers.length; i++) {
        answers[i].classList.add('edge-compliant');
    }

    var questions = document.querySelectorAll('.question > summary');
    for (var j = 0; j < questions.length; j++) {
        questions[j].addEventListener('click', e => {
            var answer = e.target.closest('.question').querySelector('.answer');
            if (answer.classList.contains('open')) {
                answer.classList.remove('open');
            } else {
                answer.classList.add('open');
            }
        });
    }
}

function emailSubmit(evt) {
    evt.preventDefault();
    evt.target.getElementsByTagName('label')[0].innerHTML =
        'GET UPDATES <div class="lds-ring"><div></div><div></div><div></div><div></div></div>';
    let email = evt.target.elements['email'].value;
    fetch(
        'https://script.google.com/macros/s/AKfycbyuewO_-jd5JWwqvpmDHaHRvjUDVCdg2MA-cckK2y43QLKlZUOA/exec',
        {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/json',
            },
            redirect: 'follow',
            body: JSON.stringify({ email_address: email }),
        }
    )
        .then(_resp => {
            evt.target.getElementsByTagName('label')[0].innerHTML =
                'GET UPDATES <div class="check"></div>';
            Array.prototype.forEach.call(evt.target.elements, elem => {
                elem.readOnly = true;
                elem.disabled = true;
                elem.value = '';
            });
        })
        .catch(_resp => {
            alert(
                'Request failed due to a network error. ' +
                    'This could mean your browser is blocking a ' +
                    'cross-origin request to google, where we store our ' +
                    'mailing list.'
            );
            evt.target.getElementsByTagName('label')[0].innerHTML =
                'GET UPDATES &#10006;';
        });
}
document.getElementById('update-form').addEventListener('submit', emailSubmit);
