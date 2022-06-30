/*global moment, firebase, */
const announcementsRef = document.getElementById('announcements');
const year = ' 2022';
// Initialize Firebase
var config = {
    apiKey: 'AIzaSyAAUV4ajWz1dqTn7rYe3rY6EFaEqS0ESaE',
    authDomain: 'los-altos-hacks-dashboard.firebaseapp.com',
    projectId: 'los-altos-hacks-dashboard',
    storageBucket: 'los-altos-hacks-dashboard.appspot.com',
    messagingSenderId: '374146820209',
    appId: '1:374146820209:web:c3fca2886ea45e9add13d0',
    measurementId: 'G-3JVKDS9408',
};
firebase.initializeApp(config);
const db = firebase.firestore();
const dbEventsRef = db.collection('events');

dbEventsRef.orderBy('timePosted', 'desc').onSnapshot(docs => {
    let regularAnnouncements = '';
    let pinnedAnnoucements = '';
    docs.forEach(doc => {
        const announcementHTML = `
      <div class="announcement ">
          <h3>${doc.data().name}</h3>
          <p>${doc.data().content}</p>
          <footer>
            ${doc.data().isPinned ? `<i class="fas fa-thumbtack"></i>` : ``}
            <date>${moment(doc.data().timePosted.toDate()).calendar()}</date>
          </footer>
      </div>
    `;
        if (doc.data().isPinned) {
            pinnedAnnoucements += announcementHTML;
        } else {
            regularAnnouncements += announcementHTML;
        }
    });
    announcementsRef.innerHTML = pinnedAnnoucements + regularAnnouncements;
});
const modalBtn = document.getElementById('request-notifications');
const closeModalPanel = document.getElementById('closeModalPanel');
const closeModalBtn = document.getElementById('closeModalBtn');
modalBtn.addEventListener('click', () => {
    const modal = document.getElementById('mapModal');
    modal.style = 'visibility: visible; opacity: 1';
});
closeModalPanel.addEventListener('click', () => {
    const modal = document.getElementById('mapModal');
    modal.style = 'visibility: hidden; opacity: 0';
});
closeModalBtn.addEventListener('click', () => {
    const modal = document.getElementById('mapModal');
    modal.style = 'visibility: hidden; opacity: 0';
});

//schedules
const updateScheduleCountDown = () => {
    const day = Schedules[moment().format('MMMM D')];
    const currEventNameElem = document.getElementById('current-event-name');
    const nextEventNameElem = document.getElementById('next-event-name');
    const nextEventCountdownElem = document.getElementById('next-event-time');
    const scheduleParent = document.getElementById('schedule');
    let currEvent = 'No Curent event';
    let currEventIndex = null;
    let minDiff = null;
    if (day) {
        day.sched.map((event, i) => {
            const localTime = moment(day.day + ' ' + event.time + year);
            const today = moment();
            const diff = localTime.diff(today);
            if (diff < 0) {
                if (minDiff) {
                    if (Math.abs(diff) < Math.abs(minDiff)) {
                        minDiff = diff;
                        currEvent = event;
                        currEventIndex = i;
                    }
                } else {
                    minDiff = diff;
                    currEvent = event;
                    currEventIndex = i;
                }
            }
        });
        let nextEvent = day.sched[currEventIndex + 1];
        let timeTillNextEvent = null;
        if (!nextEvent) {
            let nextDay =
                Schedules[
                    moment()
                        .add(1, 'days')
                        .format('MMMM D')
                ];
            if (nextDay) {
                nextEvent = nextDay.sched[0];

                timeTillNextEvent = moment().to(
                    moment(nextDay.day + ' ' + nextEvent.time + year)
                );
            }
        } else {
            timeTillNextEvent = moment().to(
                moment(day.day + ' ' + nextEvent.time + year)
            );
        }
        currEventNameElem.innerHTML = currEvent.name;
        nextEventNameElem.innerHTML = nextEvent.name;
        nextEventCountdownElem.innerHTML = timeTillNextEvent;
    } else {
        scheduleParent.style = 'display : none';
    }
};
updateScheduleCountDown();
setInterval(function() {
    updateScheduleCountDown();
}, 6000);
