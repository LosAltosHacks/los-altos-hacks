var eventsList = document.querySelectorAll('#schedule-table tbody > tr');
var clockTime = 0;
var events = [];

window.onscroll = _ => navBarDisplay();
document
    .querySelector('nav .nav-icon')
    .addEventListener('click', _ => navMenuToggle());
navBarDisplay();

registerEvents();

// Adapt to Microsoft Edge
if (!/*@cc_on!@*/ (false || !!document.documentMode)) {
    adaptEdge();
}

function navBarDisplay() {
    var nav = document.getElementsByTagName('nav')[0];
    var offset = document.getElementById('mission').offsetTop;

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
        document.querySelector('nav > .container').style.boxShadow = 'none';
        nav.style.transition = 'none';
        nav.style.top = '-100%';
        nav.style.position = 'fixed';
        if (
            document
                .getElementsByClassName('nav-icon')[0]
                .classList.contains('close')
        )
            navMenuToggle();
    } else {
        nav.style.position = 'fixed';
        nav.style.transition = 'top 0.5s';
        document.querySelector('nav > .container').style.boxShadow =
            '0 2px 3px rgba(0, 0, 0, 0.2)';
        nav.style.top = '0';
    }
}

function navMenuToggle() {
    var icon = document.getElementsByClassName('nav-icon')[0];
    var links = document.getElementsByClassName('nav-sections')[0];
    if (icon.classList.contains('close')) {
        // When the menu is open
        icon.classList.remove('close');
        links.classList.remove('open');
    } else {
        icon.classList.add('close');
        links.classList.add('open');
    }
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
        if (events[i].time <= clockTime && events[i + 1].time > clockTime) {
            eventsList[i].classList = 'active';
            var parameters = document.querySelector('#clock > .content')
                .children;
            parameters[0].textContent = events[i].day;
            parameters[2].textContent = events[i].name;
            parameters[3].textContent = events[i].location;
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

var s0 = document.getElementById("question0");
var s1 = document.getElementById("question1");
var s2 = document.getElementById("question2");
var s3 = document.getElementById("question3");
var s4 = document.getElementById("question4");
var s5 = document.getElementById("question5");
var s6 = document.getElementById("question6");
var s7 = document.getElementById("question7");
var s8 = document.getElementById("question8");
var s9 = document.getElementById("question9");

s0.onclick = function(event){
    animateDown(0, 105);
}

s1.onclick = function(event){
    animateDown(1, 126);
}

s2.onclick = function(event){
    animateDown(2, 105);
}

s3.onclick = function(event){
    animateDown(3, 105);
}

s4.onclick = function(event){
    animateDown(4, 63);
}

s5.onclick = function(event){
    animateDown(5, 105);
}

s6.onclick = function(event){
    animateDown(6, 105);
}

s7.onclick = function(event){
    animateDown(7, 63);
}

s8.onclick = function(event){
    animateDown(8, 63);
}

s9.onclick = function(event){
    animateDown(9, 63);
}


function animateDown(number, maxHeight){
    var doc = document.getElementById("answer" + number);
    console.log(doc.classList);

    if(!doc.classList.contains("open")){
        // s1.style.height = "0px";
        //setInterval(function (){height(0)}, 50);
        //how do you close this????
    } else {
        doc.style.height = "0px";
        setInterval(function (){height(maxHeight)}, 10);
    }

    function height(val){
        doc.style.height = val + "px";
    }
}