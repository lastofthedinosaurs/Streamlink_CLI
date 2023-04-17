# Get Videos

Gets information about one or more published videos. You may get videos by ID, by user, or by game/category.

You may apply several filters to get a subset of the videos. The filters are applied as an AND operation to each video. For example, if language is set to ‘de’ and game_id is set to 21779, the response includes only videos that show playing League of Legends by users that stream in German. The filters apply only if you get videos by user ID or game ID.

[https://dev.twitch.tv/docs/api/reference/#get-games](https://dev.twitch.tv/docs/api/reference/#get-games)

## Authorization

Requires an `app access token` or `user access token`.

## URL

`GET https://api.twitch.tv/helix/videos`

## Request Query Parameters

The `id`, `user_id`, and `game_id` parameters are mutually exclusive.

| Parameter | Type     | Required? | Description                                                                                                                                                                                                                                                                                                                                          |
|-----------|----------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id        | string   | Yes       | A list of IDs that identify the videos you want to get. To get more than one video, include this parameter for each video you want to get. For example, id=1234&id=5678. You may specify a maximum of 100 IDs. The endpoint ignores duplicate IDs and IDs that weren’t found (if there’s at least one valid ID).                                     |
| user_id   | String   | Yes       | The ID of the user whose list of videos you want to get.                                                                                                                                                                                                                                                                                             |
| game_id   | String   | Yes       | A category or game ID. The response contains a maximum of 500 videos that show this content. To get category/game IDs, use the [Search Categories](https://dev.twitch.tv/docs/api/reference/#search-categories) endpoint.                                                                                                                            |
| language  | String   | No        | A filter used to filter the list of videos by the language that the video owner broadcasts in. For example, to get videos that were broadcast in German, set this parameter to the ISO 639-1 two-letter code for German (i.e., DE). For a list of supported languages, see Supported Stream Language. If the language is not supported, use “other.” |
| period    | String   | No        | A filter used to filter the list of videos by when they were published. For example, videos published in the last week. Possible values are: `all`, `day`, `month`, and `week`. The default is “all,” which returns videos published in all periods. Specify this parameter only if you specify the game_id or user_id query parameter.              |
| sort      | String   | No        | The order to sort the returned videos in. Possible values are: `time`, `trending`, and `views`. Sort the results in descending order by most views (i.e., highest number of views first). The default is `time`. Specify this parameter only if you specify the `game_id` or `user_id` query parameter.                                              |
| type      | String   | No        | A filter used to filter the list of videos by the video’s type. Possible case-sensitive values are: `all`, `archive`, `highlight`, and `upload`. The default is `all`, which returns all video types. Specify this parameter only if you specify the `game_id` or `user_id` query parameter.                                                         |
| first     | Integer  | No        | The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 25 items per page. The default is 20.                                                                                                                                                                                    |
| after     | String   | No        | The cursor used to get the next page of results. The Pagination object in the response contains the cursor’s value. [Read More](https://dev.twitch.tv/docs/api/guide#pagination).                                                                                                                                                                    |
| before    | String   | No        | The cursor used to get the previous page of results. The Pagination object in the response contains the cursor’s value. [Read more](https://dev.twitch.tv/docs/api/guide#pagination).                                                                                                                                                                |


## Example Request

Gets information about the specified video.

``` bash
curl -X GET 'https://api.twitch.tv/helix/videos?id=335921245' \
    -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
```

## Example Response

``` json
{
  "data": [
    {
      "id": "335921245",
      "stream_id": null,
      "user_id": "8675309",
      "user_login": "lastofthedinosaurs",
      "user_name": "LastoftheDinosaurs",
      "title": "Twitch Developers 101",
      "description": "Welcome to Twitch development! Here is a quick overview and information to help you get started.",
      "created_at": "2018-11-14T21:30:18Z",
      "published_at": "2018-11-14T22:04:30Z",
      "url": "https://www.twitch.tv/videos/335921245",
      "thumbnail_url": "https://static-cdn.jtvnw.net/cf_vods/d2nvs31859zcd8/twitchdev/335921245/ce0f3a7f-57a3-4152-bc06-0c6610189fb3/thumb/index-0000000000-%{width}x%{height}.jpg",
      "viewable": "public",
      "view_count": 1863062,
      "language": "en",
      "type": "upload",
      "duration": "3m21s",
      "muted_segments": [
        {
          "duration": 30,
          "offset": 120
        }
      ]
    }
  ],
  "pagination": {}
}
```
