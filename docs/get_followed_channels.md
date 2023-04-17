# Get Followed Channels

Gets a list of broadcasters that the specified user follows. You can also use this endpoint to see whether a user follows a specific broadcaster.

[https://dev.twitch.tv/docs/api/reference/#get-followed-channels](https://dev.twitch.tv/docs/api/reference/#get-followed-channels)

## Authorization

Requires a `user access token` that includes the `user:read:follows` scope.

## URL

`GET https://api.twitch.tv/helix/channels/followed`

## Request Query Parameters

| Parameter      | Type     | Required? | Description                                                                                                                                                                                                                                             |
|----------------|----------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user_id        | String   | No        | A user’s ID. Returns the list of broadcasters that this user follows. This ID must match the user ID in the user OAuth token.                                                                                                                           |
| broadcaster_id | String   | Yes       | A broadcaster’s ID. Use this parameter to see whether the user follows this broadcaster. If specified, the response contains this broadcaster if the user follows them. If not specified, the response contains all broadcasters that the user follows. |
| first          | Integer  | No        | The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 100. The default is 20.                                                                                                     |
| after          | String   | No        | The cursor used to get the next page of results. The Pagination object in the response contains the cursor’s value. [Read more](https://dev.twitch.tv/docs/api/guide#pagination).                                                                       |

## Example Request

Gets the list of broadcasters that the specified user follows.

``` bash
curl -X GET 'https://api.twitch.tv/helix/channels/followed?user_id=123456' \
    -H 'Authorization: Bearer kpvy3cjboyptmiacwr0c19hotn5s' \
    -H 'Client-Id: hof5gwx0su6owfn0nyan9c87zr6t'
```

## Example Response

``` json
{
  "total": 8
  "data": [
    {
      "broadcaster_id": "11111",
      "broadcaster_login": "userloginname",
      "broadcaster_name": "UserDisplayName",
      "followed_at": "2022-05-24T22:22:08Z",
    },
    ...
  ],
  "pagination": {
    "cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6NX19"
  }
}
```

## Example Request

Checks whether the specified user follows the specified broadcaster.

``` bash
curl -X GET 'https://api.twitch.tv/helix/channels/followers?user_id=123456&broadcaster_id=654321' \
    -H 'Authorization: Bearer kpvy3cjboyptmiacwr0c19hotn5s' \
    -H 'Client-Id: hof5gwx0su6owfn0nyan9c87zr6t'
```

## Example Response

The data field is not an empty array, which means that the user does follow the specified broadcaster.

``` json
{
  "total": 8
  "data": [
    {
      "broadcaster_id": "654321",
      "broadcaster_login": "basketweaver101",
      "broadcaster_name": "BasketWeaver101",
      "followed_at": "2022-05-24T22:22:08Z",
    }
  ],
  "pagination": {}
}
```