# Registration Server 2019

## Endpoints

### Attendee Registration

#### `/attendees/` `POST`
```js
{
  // required:
  "first_name": "...",
  "last_name": "...",
  "email": "name@example.com",
  "phone_number": "(123) 456-7890",
  "age": 18,
  "education": "High School",
  "tshirt_size": "S", // Can be "S", "M", "L" or "XL"

  // required if school == "High School" | school == "Middle School"
  "school": "Los Altos High School",

  // required if age is under 18:
  "guardian_name": "...",
  "guardian_email": "...",
  "guardian_phone_number": "(123) 456-7890",

  // optional:
  "special": "...",
  "goals": "...",
  "gender": "Female",
  "ethnicity": "Asian",
  "previous_hackathons": 4,
  "github_username": "...",
  "linkedin_profile": "...",
  "dietary_restrictions": "..."
}
```

### Mentor Registration

#### `/mentors/` `POST`
```js
{
  // required:
  "first_name": "...",
  "last_name": "...",
  "email": "name@example.com",
  "phone_number": "(123) 456-7890",
  "over_18": true,
  "company": "...",
  "timeslots": [
    {
      "start_time": "2020-03-21T09:00",
      "end_time": "2020-03-22T12:00"
    }
  ],
  "tshirt_size": "S", // Can be "S", "M", "L" or "XL"

  // optional:
  "skillset": "..."
  "dietary_restrictions": "..."
}
```

### Guest Registration

#### Sponsor `/sponsors/` `POST`
```js
{
  // required:
  "first_name": "...",
  "last_name": "...",
  "email": "name@example.com",
  "phone_number": "(123) 456-7890",
  "company": "..."
  "tshirt_size": "S", // Can be "S", "M", "L" or "XL"

  // optional:
  "purpose": "...",
  "dietary_restrictions": "..."
}
```

#### VIP `/vip/` `POST`
```js
{
  // required:
  "first_name": "...",
  "last_name": "...",
  "email": "name@example.com",
  "phone_number": "(123) 456-7890",
  "company": "..."
  "tshirt_size": "S", // Can be "S", "M", "L" or "XL"

  // optional:
  "purpose": "...",
  "dietary_restrictions": "..."
}
```

#### Chaperone `/chaperones/` `POST`
```js
{
  // required:
  "first_name": "...",
  "last_name": "...",
  "email": "name@example.com",
  "phone_number": "(123) 456-7890",
  "timeslots": [
    {
      "start_time": "2020-03-21T09:00",
      "end_time": "2020-03-22T12:00"
    }
  ],
  "tshirt_size": "S", // Can be "S", "M", "L" or "XL"

  // optional:
  "purpose": "...",
  "dietary_restrictions": "..."
}
```

#### `/attendees/verify/<user_id>/<email_token>/` `GET`

Verifies the attendee's email

#### `/<guest_type>/` `GET`

Lists all signups where `outdated=False`

#### `/<guest_type>/<user_id>/` `DELETE`

Deletes the user

#### `/<guest_type>/<user_id>/` `PATCH`

Modifies the user data

#### `/<guest_type>/search/` `GET`

Searches for a user

#### `/<guest_type>/<user_id>/history/` `GET`

Gets the history (all `outdated=True` and `outdated=False` signups) for a user