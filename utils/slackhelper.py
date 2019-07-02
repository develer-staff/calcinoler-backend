from slack import WebClient, errors


class SlackHelper:
    def __init__(self, token):
        self.slack_client = WebClient(token=token)

    def get_users(self, search=None, field=None) -> list:
        try:
            resp = self.slack_client.users_list()
        except errors.SlackApiError as e:
            raise SlackRequestFailed(e)
        if not resp['ok']:
            raise SlackRequestFailed("'ok' flag is false")
        slack_users = resp['members']
        if search:
            slack_users = self.search_user(slack_users, search)
        if field:
            return [u[field] for u in slack_users if field in u]
        return slack_users

    def get_user(self, slack_id):
        try:
            resp = self.slack_client.users_profile_get(user=slack_id)
        except errors.SlackApiError as e:
            raise SlackRequestFailed(e)
        if not resp['ok']:
            raise SlackRequestFailed("'ok' flag is false")
        return resp['profile']

    @staticmethod
    def search_user(self, users, search) -> list:
        res = []
        for u in users:
            for v in u:
                if search in v:
                    res.append(u)
                    continue
        return res


class SlackRequestFailed(Exception):
    pass
