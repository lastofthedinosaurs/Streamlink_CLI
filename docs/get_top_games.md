# Get Top Games

Gets information about all broadcasts on Twitch.

[https://dev.twitch.tv/docs/api/reference/#get-top-games](https://dev.twitch.tv/docs/api/reference/#get-top-games)

## Authorization

Requires an `app access token` or `user access token`.

## URL

`GET https://api.twitch.tv/helix/games/top`

## Request Query Parameters

| Parameter  | Type     | Required?  | Description                                                                                                                                                                           |
|------------|----------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| first      | Integer  | No         | The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 100 items per page. The default is 20.                    |
| before     | String   | No         | The cursor used to get the previous page of results. The Pagination object in the response contains the cursor’s value. [Read more](https://dev.twitch.tv/docs/api/guide#pagination). |
| after      | String   | No         | The cursor used to get the next page of results. The Pagination object in the response contains the cursor’s value. [Read more](https://dev.twitch.tv/docs/api/guide#pagination).     |


## Example Request

``` bash
curl -X GET 'https://api.twitch.tv/helix/games/top' \
    -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
```

## Example Response

``` json
{
  "data": [
    {
      "id": "493057",
      "name": "PUBG: BATTLEGROUNDS",
      "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/493057-{width}x{height}.jpg",
      "igdb_id": "27789"
    },
    ...
  ],
  "pagination":{"cursor":"eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ=="}
}
```
