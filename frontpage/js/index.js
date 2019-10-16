var eventsList = document.querySelectorAll('#schedule-table tbody > tr');
var clockTime = 0;
var events = [];

window.onresize = _ => adjustHeaderDisplay();
window.onscroll = _ => navBarDisplay();
navBarDisplay();

adjustHeaderDisplay();
registerEvents();

for (let question of document.querySelectorAll('.question')) {
    question.addEventListener('toggle', e => {
        // var q = e.path.filter(elem => {
        //     return elem.tagName == 'DETAILS';
        // })[0];
        // console.log(e);
        // var originalHeight = q.offsetHeight;
        // console.log(originalHeight);
        // var open = q.getAttribute('open') != null;
        //
        // if (open) {
        //     q.style.height = originalHeight;
        //     setTimeout(_ => {
        //         console.log('hi');
        //         q.style.height = '100%';
        //     }, 520);
        // } else {
        //     q.style.height = null;
        // }
    });
}

function navBarDisplay() {
    var nav = document.getElementsByTagName('nav')[0];
    var offset = document.getElementById('mission').offsetTop;
    console.log(offset);

    if (
        document.body.scrollTop <= 50 &&
        document.documentElement.scrollTop <= 50
    ) {
        nav.style.top = '0';
        nav.style.position = 'absolute';
    } else if (
        (document.body.scrollTop > 50 ||
            document.documentElement.scrollTop > 50) &&
        (document.body.scrollTop < offset &&
            document.documentElement.scrollTop < offset)
    ) {
        nav.style.boxShadow = 'none';
        nav.style.transition = 'none';
        nav.style.top = '-100%';
        nav.style.position = 'fixed';
    } else {
        nav.style.transition = 'top 0.5s';
        nav.style.boxShadow = '0 2px 3px rgba(0, 0, 0, 0.2)';
        nav.style.top = '0';
    }
}

// Adjust table header display
function adjustHeaderDisplay() {
    console.log(
        document.querySelector('#schedule-table .sunday tbody tr').clientWidth
    );

    document.querySelector(
        '#schedule-table .saturday thead th:first-child'
    ).style.width = `${
        document.querySelector('#schedule-table .saturday tbody td:first-child')
            .offsetWidth
    }px`;

    document.querySelector(
        '#schedule-table .saturday thead th:last-child'
    ).style.width = `${document.querySelector('#schedule-table .saturday tbody')
        .offsetWidth -
        document.querySelector('#schedule-table .saturday tbody td:first-child')
            .offsetWidth}px`;

    document.querySelector(
        '#schedule-table .sunday thead th:first-child'
    ).style.width = `${
        document.querySelector('#schedule-table .sunday tbody td:first-child')
            .offsetWidth
    }px`;

    document.querySelector(
        '#schedule-table .sunday thead th:last-child'
    ).style.width = `${document.querySelector('#schedule-table .sunday tbody')
        .offsetWidth -
        document.querySelector('#schedule-table .sunday tbody td:first-child')
            .offsetWidth}px`;
}

// Register all events
function registerEvents() {
    // Compile events into a list
    for (var i = 0; i < eventsList.length; i++) {
        var node = eventsList[i];

        var day = node.parentNode.parentNode.parentNode.parentNode.classList.contains(
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

    document
        .querySelector('#schedule-table .sunday span.left')
        .addEventListener('click', e => {
            document.querySelector('#schedule-table .sunday').style.display =
                'none';
            document.querySelector('#schedule-table .saturday').style.display =
                'unset';

            adjustHeaderDisplay();
        });

    document
        .querySelector('#schedule-table .saturday span.right')
        .addEventListener('click', e => {
            document.querySelector('#schedule-table .saturday').style.display =
                'none';
            document.querySelector('#schedule-table .sunday').style.display =
                'unset';

            adjustHeaderDisplay();
        });

    // Register scrolling listener for clock
    document.getElementById('clock').addEventListener('wheel', e => {
        // To prevent discrepancy between rotation animation and scrolling
        document.querySelector(
            '#hour-pointer > span, #minute-pointer > span'
        ).style.transition = 'none';

        if (e.deltaY == 0) return;
        clockTime += e.deltaY < 0 ? -5 : 5;

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

        adjustHeaderDisplay();
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

        adjustHeaderDisplay();
    }

    // Update table according to time
    eventsList.forEach(node => {
        node.classList.remove('active'); // Reset active item
    });

    for (var i = 0; i < events.length - 1; i++) {
        if (events[i].time <= clockTime && events[i + 1].time > clockTime) {
            eventsList[i].classList = 'active';
            var parameters = document.querySelector('#clock > .content')
                .children;
            parameters[0].textContent = events[i].day;
            parameters[2].textContent = events[i].name;
            parameters[3].textContent = events[i].location;
            // document.querySelector('#schedule-table tbody').scrollTop =
            //     eventsList[i].offsetTop - eventsList[i].offsetHeight;
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
