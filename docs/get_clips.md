# Get Clips

Gets one or more video clips that were captured from streams. For information about clips, see [How to use clips](https://help.twitch.tv/s/article/how-to-use-clips).

[https://dev.twitch.tv/docs/api/reference/#get-clips](https://dev.twitch.tv/docs/api/reference/#get-clips)

## Authorization

Requires an `app access token` or `user access token`.

## URL

`GET https://api.twitch.tv/helix/clips`

## Request Query Parameters

The `id`, `game_id`, and `broadcaster_id` query parameters are mutually exclusive.


| Parameter      | Type    | Required? | Description                                                                                                                                                                                                                                             |
|----------------|---------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| broadcaster_id | String  | Yes       | A broadcaster’s ID. Use this parameter to see whether the user follows this broadcaster. If specified, the response contains this broadcaster if the user follows them. If not specified, the response contains all broadcasters that the user follows. |
| game_id        | String  | Yes       | An ID that identifies the game whose clips you want to get. Use this parameter to get clips that were captured from streams that were playing this game.                                                                                                |
| id             | String  | Yes       | An ID that identifies the clip to get. To specify more than one ID, include this parameter for each clip you want to get. For example, `id=foo&id=bar`. You may specify a maximum of 100 IDs. The API ignores duplicate IDs and IDs that aren’t found.  |
| started_at     | String  | No        | The start date used to filter clips. The API returns only clips within the start and end date window. Specify the date and time in RFC3339 format.                                                                                                      |
| ended_at       | String  | No        | The end date used to filter clips. If not specified, the time window is the start date plus one week. Specify the date and time in RFC3339 format.                                                                                                      |
| first          | Integer | No        | The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 100. The default is 20.                                                                                                     |
| before         | String  | No        | The cursor used to get the previous page of results. The Pagination object in the response contains the cursor’s value. [Read More](https://dev.twitch.tv/docs/api/guide#pagination).                                                                   |
| after          | String  | No        | The cursor used to get the next page of results. The Pagination object in the response contains the cursor’s value. [Read more](https://dev.twitch.tv/docs/api/guide#pagination).                                                                       |

## Example Request

Gets a clip by ID.

``` bash
curl -X GET 'https://api.twitch.tv/helix/clips?id=AwkwardHelplessSalamanderSwiftRage' \
    -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
```

## Example Response

``` json
{
  "data": [
    {
      "id": "AwkwardHelplessSalamanderSwiftRage",
      "url": "https://clips.twitch.tv/AwkwardHelplessSalamanderSwiftRage",
      "embed_url": "https://clips.twitch.tv/embed?clip=AwkwardHelplessSalamanderSwiftRage",
      "broadcaster_id": "67955580",
      "broadcaster_name": "ChewieMelodies",
      "creator_id": "53834192",
      "creator_name": "BlackNova03",
      "video_id": "205586603",
      "game_id": "488191",
      "language": "en",
      "title": "babymetal",
      "view_count": 10,
      "created_at": "2017-11-30T22:34:18Z",
      "thumbnail_url": "https://clips-media-assets.twitch.tv/157589949-preview-480x272.jpg",
      "duration": 60,
      "vod_offset": 480
    }
  ]
}
```

## Example Request

Gets the broadcaster’s top 5 clips based on views.

``` bash
curl -X GET 'https://api.twitch.tv/helix/channels/followers?user_id=123456&broadcaster_id=654321' \
    -H 'Authorization: Bearer kpvy3cjboyptmiacwr0c19hotn5s' \
    -H 'Client-Id: hof5gwx0su6owfn0nyan9c87zr6t'
```

## Example Response

``` json
{
  "data": [
    {
      "id": "RandomClip1",
      "url": "https://clips.twitch.tv/AwkwardHelplessSalamanderSwiftRage",
      "embed_url": "https://clips.twitch.tv/embed?clip=RandomClip1",
      "broadcaster_id": "1234",
      "broadcaster_name": "JJ",
      "creator_id": "123456",
      "creator_name": "MrMarshall",
      "video_id": "",
      "game_id": "33103",
      "language": "en",
      "title": "random1",
      "view_count": 10,
      "created_at": "2017-11-30T22:34:18Z",
      "thumbnail_url": "https://clips-media-assets.twitch.tv/157589949-preview-480x272.jpg",
      "duration": 12.9,
      "vod_offset": 1957
    },
    ...
  ],
  "pagination": {
    "cursor": "eyJiIjpudWxsLCJhIjoiIn0"
  }
}
```