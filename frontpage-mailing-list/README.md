# Frontpage Mailing

This is the one of the few peices of unversioned software we run.
Due to time constraints on the website, we I (Josh) setup a quick, dirty google apps script to put email into a Google Sheet
(`Tools > Script Editor`, then `Publish > Deploy as web app...`).

The script is in `Code.gs`, invoked like:

```sh
curl --request POST --data '{"email_address": "b@a.com"}' https://script.google.com/macros/s/<URI>/exec
```

or in JS:

```javascript
fetch('https://script.google.com/macros/s/<URI>/exec', {
    method: 'POST',
    mode: 'no-cors',
    headers: {
        'Content-Type': 'application/json',
    },
    redirect: 'follow',
    body: JSON.stringify({ email_address: email }),
});
```

I (Josh) will hopefully remember to update this repo if the script changes.
