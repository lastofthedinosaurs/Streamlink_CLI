# Get Users

Gets information about one or more users.

You may look up users using their user ID, login name, or both but the sum total of the number of users you may look up is 100. For example, you may specify 50 IDs and 50 names or 100 IDs or names, but you cannot specify 100 IDs and 100 names.

If you don’t specify IDs or login names, the request returns information about the user in the access token if you specify a user access token.

To include the user’s verified email address in the response, you must use a user access token that includes the user:read:email scope.

[https://dev.twitch.tv/docs/api/reference/#get-users](https://dev.twitch.tv/docs/api/reference/#get-users)

## Authorization

Requires an `app access token` or `user access token`.

## URL

`GET https://api.twitch.tv/helix/users`

## Request Query Parameters

| Parameter  | Type   | Required?  | Description                        |
|------------|--------|------------|------------------------------------|
| id         | String | No         | The ID of the user to get          |
| login      | String | No         | The login name of the user to get  |

## Example Request

Gets information about the specified user.

``` bash
curl -X GET 'https://api.twitch.tv/helix/users?id=141981764' \
    -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'

```

## Example Response

``` json
{
  "data": [
    {
      "id": "141981764",
      "login": "twitchdev",
      "display_name": "TwitchDev",
      "type": "",
      "broadcaster_type": "partner",
      "description": "Supporting third-party developers building Twitch integrations from chatbots to game integrations.",
      "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
      "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png",
      "view_count": 5980557,
      "email": "not-real@email.com",
      "created_at": "2016-12-14T20:32:28Z"
    }
  ]
}
```