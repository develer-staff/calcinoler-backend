from slack import WebClient, errors


class SlackHelper:
    """Wraps official Slack's client functions for grater dynamism.
    """

    def __init__(self, token: str):
        """Init official client.

            token (str):
                is the token for Api calls authentication.
                https://api.slack.com/start/overview
        """
        self.slack_client = WebClient(token=token)

    def get_users(self, search: str = None, field: str = None) -> list:
        """Calls Slack's endpoint `users.list`.

            search (str):
                if is not None the function returns only slack's users
                who match string at least one field.
            field (str):
                if is not None the function will return a list containing
                only specified field.

            Returns list of slack's users or
            a list of field value from Slack's Api.

            Raises SlackRequestFailed if request fail.
        """
        try:
            resp = self.slack_client.users_list()
        except errors.SlackApiError as e:
            raise SlackRequestFailed(e)
        if not resp['ok']:
            raise SlackRequestFailed(resp.get('error', 'Request failed'))
        slack_users = resp['members']
        if search:
            slack_users = self.search_user(slack_users, search)
        if field:
            return [u[field] if field in u else None for u in slack_users]
        return slack_users

    def get_user(self, slack_id: str) -> dict:
        """Calls Slack's endpoint `users.profile.get`.

            slack_id (str):
                Slack's ID.

            Returns a dict representing Slack's user.

            Raises SlackRequestFailed if request fail.
        """
        try:
            resp = self.slack_client.users_profile_get(user=slack_id)
        except errors.SlackApiError as e:
            raise SlackRequestFailed(e)
        if not resp['ok']:
            raise SlackRequestFailed(resp.get('error', 'Request failed'))
        return resp['profile']

    @staticmethod
    def __search_user(users: list, search: str) -> list:
        """Searches user by string in all fields.

            users (list(dict)):
                Slack users from Slack's Api.
            search (str):
                String to find in fields.

            Returns list(dict) representing users who match
            string at least in one field.
        """
        res = []
        for u in users:
            for v in u:
                if search in v:
                    res.append(u)
                    continue
        return res


class SlackRequestFailed(Exception):
    pass
