# Get Channel Stream Schedule

Gets the broadcaster’s streaming schedule. You can get the entire schedule or specific segments of the schedule. [Learn More](https://help.twitch.tv/s/article/channel-page-setup#Schedule).

[https://dev.twitch.tv/docs/api/reference/#get-games](https://dev.twitch.tv/docs/api/reference/#get-games)

## Authorization

Requires an `app access token` or `user access token`.

## URL

`GET https://api.twitch.tv/helix/schedule`

## Request Query Parameters

| Parameter       | Type     | Required?  | Description                                                                                                                                                                                                                                                                           |
|-----------------|----------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| broadcaster_id  | string   | No         | The ID of the broadcaster that owns the streaming schedule you want to get.                                                                                                                                                                                                           |
| id              | string   | No         | The ID of the scheduled segment to return. To specify more than one segment, include the ID of each segment you want to get. For example,  `&id=8675id=3099`. You may specify a maximum of 100 IDs.                                                                                   |
| start_time      | string   | No         | The UTC date and time that identifies when in the broadcaster’s schedule to start returning segments. If not specified, the request returns segments starting after the current UTC date and time. Specify the date and time in RFC3339 format (for example, `2022-09-01T00:00:00Z`). |
| utc_offset      | string   | No         | Not supported.                                                                                                                                                                                                                                                                        |
| first           | Integer  | No         | The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 25 items per page. The default is 20.                                                                                                                     |
| after           | String   | No         | The cursor used to get the next page of results. The Pagination object in the response contains the cursor’s value. [Read More](https://dev.twitch.tv/docs/api/guide#pagination).                                                                                                     |


## Example Request

Gets the specified broadcaster’s streaming schedule.

``` bash
curl -X GET 'https://api.twitch.tv/helix/schedule?broadcaster_id=8675309' \
    -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
```

## Example Response

``` json
{
  "data": {
    "segments": [
      {
        "id": "eyJzZWdtZW50SUQiOiJlNGFjYzcyNC0zNzFmLTQwMmMtODFjYS0yM2FkYTc5NzU5ZDQiLCJpc29ZZWFyIjoyMDIxLCJpc29XZWVrIjoyNn0=",
        "start_time": "2021-07-01T18:00:00Z",
        "end_time": "2021-07-01T19:00:00Z",
        "title": "LastoftheDinosaurs Monthly Update // July 1, 2021",
        "canceled_until": null,
        "category": {
            "id": "8675309",
            "name": "Science & Technology"
        },
        "is_recurring": false
      },
      ...
    ],
    "broadcaster_id": "8675309",
    "broadcaster_name": "LastoftheDinosaurs",
    "broadcaster_login": "lastofthedinosaurs",
    "vacation": null
  },
  "pagination": {}
}
```
