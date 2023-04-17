# Get Games

Gets information about specified categories or games.

You may get up to 100 categories or games by specifying their ID or name. You may specify all IDs, all names, or a combination of IDs and names. If you specify a combination of IDs and names, the total number of IDs and names must not exceed 100.

[https://dev.twitch.tv/docs/api/reference/#get-games](https://dev.twitch.tv/docs/api/reference/#get-games)

## Authorization

Requires an `app access token` or `user access token`.

## URL

`GET https://api.twitch.tv/helix/games`

## Request Query Parameters

| Parameter | Type   | Required?  | Description                                                                                                                                                                                                                                                                                                           |
|-----------|--------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id        | string | No         | The ID of the category or game to get. Include this parameter for each category or game you want to get. For example, `&id=8675id=3099`. You may specify a maximum of 100 IDs. The endpoint ignores duplicate and invalid IDs or IDs that weren’t found.                                                              |
| name      | String | No         | The name of the category or game to get. The name must exactly match the category’s or game’s title. Include this parameter for each category or game you want to get. For example, `&name=foo&name=bar`. You may specify a maximum of 100 names. The endpoint ignores duplicate names and names that weren’t found.  |
| igdb_id   | String | No         | The [IGDB](https://www.igdb.com/) ID of the game to get. Include this parameter for each game you want to get. For example, &igdb_id=1234&igdb_id=5678. You may specify a maximum of 100 IDs. The endpoint ignores duplicate and invalid IDs or IDs that weren’t found.                                               |


## Example Request

``` bash
curl -X GET 'https://api.twitch.tv/helix/games?id=33214' \
    -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
```

## Example Response

``` json
{
  "data": [
    {
      "id": "33214",
      "name": "Fortnite",
      "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/33214-{width}x{height}.jpg",
      "igdb_id": "1905"
    }
    ...
  ],
  "pagination": {
    "cursor": "eyJiIjpudWxsLCJhIjp7IkN"
  }
}
```
