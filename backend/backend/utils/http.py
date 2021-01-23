from django.contrib.auth.models import User
from accounts.models import Account

def query_to_dict(query):
  """
  Given query parameters, this function returns a dictionary which can be used to query a database.
  """
    search = {}
    for key in query:
        val = ""
        if query[key] == "false":
            val = False
        elif query[key] == "true":
            val = True
        elif key == "username":
            user = User.objects.get(username=query[key])
            account = Account.objects.get(user=user)
            val = account
            key = "creator"
        else:
            val = query[key]
        search[key] = val
    return search