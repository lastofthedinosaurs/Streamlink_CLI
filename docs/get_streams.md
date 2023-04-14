# Get Streams

Gets a list of all streams. The list is in descending order by the number of viewers watching the stream. Because viewers come and go during a stream, it’s possible to find duplicate or missing streams in the list as you page through the results.

[https://dev.twitch.tv/docs/api/reference/#get-streams](https://dev.twitch.tv/docs/api/reference/#get-streams)

## URL

`GET https://api.twitch.tv/helix/streams`

## Request Query Parameters

| Parameter  | Type     | Required?  | Description                    |
|------------|----------|------------|--------------------------------|
| user_id    | String   | No         |                                |
| user_login | String   | No         |                                |
| game_id    | String   | No         |                                |
| type       | String   | No         | all or live                    |
| language   | String   | No         | Two-letter language code       |
| first      | Integer  | No         | Number of results on 1st page  |
| before     | String   | No         | Get the previous page          |
| after      | String   | No         | Get the next page              |

## Get information about the 20 most active streams 

### Example Request

``` bash
curl -X GET 'https://api.twitch.tv/helix/streams' \
    -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
    -H 'Client-Id: wbmytr93xzw8zbg0p1izqyzzc5mbiz'

```

### Example Response

``` json
{
  "data": [
    {
      "id": "123456789",
      "user_id": "98765",
      "user_login": "sandysanderman",
      "user_name": "SandySanderman",
      "game_id": "494131",
      "game_name": "Little Nightmares",
      "type": "live",
      "title": "hablamos y le damos a Little Nightmares 1",
      "tags": ["Español"],
      "viewer_count": 78365,
      "started_at": "2021-03-10T15:04:21Z",
      "language": "es",
      "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_auronplay-{width}x{height}.jpg",
      "tag_ids": [],
      "is_mature": false
    },
    ...
  ],
  "pagination": {
    "cursor": "eyJiIjp7IkN1cnNvciI6ImV5SnpJam8zT0RNMk5TNDBORFF4TlRjMU1UY3hOU3dpWkNJNlptRnNjMlVzSW5RaU9uUnlkV1Y5In0sImEiOnsiQ3Vyc29yIjoiZXlKeklqb3hOVGs0TkM0MU56RXhNekExTVRZNU1ESXNJbVFpT21aaGJITmxMQ0owSWpwMGNuVmxmUT09In19"
  }
}
```

## Get streams for the specified logins

### Example Request

``` bash
curl -X GET 'https://api.twitch.tv/helix/streams' \
    -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
    -H 'Client-Id: wbmytr93xzw8zbg0p1izqyzzc5mbiz'

```

### Example Response

If the user is not live, the response doesn’t include them. 

``` json
{
  "data": [
    {
      "id": "123456789",
      "user_id": "98765",
      "user_login": "sandysanderman",
      "user_name": "SandySanderman",
      "game_id": "494131",
      "game_name": "Little Nightmares",
      "type": "live",
      "title": "hablamos y le damos a Little Nightmares 1",
      "tags": ["Español"],
      "viewer_count": 78365,
      "started_at": "2021-03-10T15:04:21Z",
      "language": "es",
      "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_auronplay-{width}x{height}.jpg",
      "tag_ids": [],
      "is_mature": false
    },
    ...
  ],
  "pagination": {
    "cursor": "eyJiIjp7IkN1cnNvciI6ImV5SnpJam8zT0RNMk5TNDBORFF4TlRjMU1UY3hOU3dpWkNJNlptRnNjMlVzSW5RaU9uUnlkV1Y5In0sImEiOnsiQ3Vyc29yIjoiZXlKeklqb3hOVGs0TkM0MU56RXhNekExTVRZNU1ESXNJbVFpT21aaGJITmxMQ0owSWpwMGNuVmxmUT09In19"
  }
}
```