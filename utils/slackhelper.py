from slack import WebClient, errors


class SlackHelper:
    """Wraps official Slack client functions and add the following
        additional features:

        - search in users list
        - extract only one field
    """

    def __init__(self, token: str):
        """Init official client.

            token (str):
                is the token for Api calls authentication.
                https://api.slack.com/start/overview
        """
        self.slack_client = WebClient(token=token)

    def get_users(self, search: str = None, field: str = None) -> list:
        """Return all Slack users.

            search (str):
                if not None the function returns only Slack users
                who contains the given string at least in one field.
            field (str):
                if not None the function returns a list containing
                only the specified field.

            Returns a list of Slack users or
            a list of field values from the Slack Api.

            Raises SlackRequestFailed if error occured.
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
        """Return a Slack user by slack_id.

            slack_id (str):
                Slack user ID.

            Returns a dict representing Slack user.

            Raises SlackRequestFailed if error occured.
        """
        try:
            resp = self.slack_client.users_profile_get(user=slack_id)
        except errors.SlackApiError as e:
            raise SlackRequestFailed(e)
        if not resp['ok']:
            raise SlackRequestFailed(resp.get('error', 'Request failed'))
        return resp['profile']

    @staticmethod
    def _search_user(users: list, search: str) -> list:
        """Searches user by string in all fields.

            users (list(dict)):
                Slack users from Slack Api.
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
