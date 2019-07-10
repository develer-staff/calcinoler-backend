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

    def get_users(self, search: str = None) -> list:
        """Return all Slack users.

            search (str):
                if not None the function returns only Slack users
                who contains the given string at least in one field.

            Returns a list of Slack users or
            a list of field values from the Slack Api.

            Raises SlackRequestFailed if error occured.
        """
        try:
            resp = self.slack_client.users_list()
        except errors.SlackApiError as e:
            raise SlackRequestFailed(e.response.get('error', 'unknown_error'))
        slack_users = resp['members']
        if search:
            slack_users = SlackHelper._search_user(slack_users, search)
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
            err = e.response.get('error', 'unknown_error')
            if err == "user_not_found":
                raise SlackUserNotFound(e)
            raise SlackRequestFailed(e)
        return resp['profile']

    @staticmethod
    def _search_user(users: list, search: str) -> list:
        """Searches user by string in all fields.
            No deep search.

            users (list(dict)):
                Slack users from Slack Api.
            search (str):
                String to find in fields.

            Returns list(dict) representing users who match
            string at least in one field.
        """
        res = []
        for user in users:
            for key in user:
                if user not in res:
                    try:
                        if search in user[key]:
                            res.append(user)
                    except Exception:
                        pass
        return res


class SlackRequestFailed(Exception):
    pass


class SlackUserNotFound(Exception):
    pass
