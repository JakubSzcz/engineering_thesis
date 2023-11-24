# NOT IN USE
# implements caching system for retrieving already authorized tokens, deprecated

# library imports
from datetime import datetime
from typing import List
import threading

# package imports
from models.user import CachedUserInfo
from models.auth import CachedTokenInfo


# Singleton class declaration
class Cache(object):

    _lock = threading.Lock()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)
        return cls.instance

    cached_users: List[CachedUserInfo] = []
    cached_tokens: List[CachedTokenInfo] = []

    def add_user_to_cache(self, user: CachedUserInfo):
        with self._lock:
            self.cached_users.append(user)
            print(self.cached_users)

    def add_token_to_cache(self, token: CachedTokenInfo):
        with self._lock:
            self.cached_tokens.append(token)

    def remove_users_from_cache(self, index: int):
        with self._lock:
            self.cached_users = self.cached_users[index + 1:]

    def remove_tokens_from_cache(self, index: int):
        with self._lock:
            self.cached_tokens = self.cached_tokens[index + 1:]

    def is_token_valid(self, token: str):
        for token_instance in self.cached_tokens:
            if token_instance.token == token and token_instance.expiration_date < datetime.now():
                return True
            else:
                self.cached_tokens.remove(token_instance)
                self.clear_cache()
                return False

    def is_client_already_authenticated(self, client_id: str):
        for user_instance in self.cached_users:
            if user_instance.client_id == client_id and user_instance.expiration_date < datetime.now():
                return True
            else:
                self.cached_users.remove(user_instance)
                self.clear_cache()
                return False

    def clear_cache(self):
        users_empty = len(self.cached_users) == 0
        tokens_empty = len(self.cached_tokens) == 0
        # clear cached users info
        timestamp = datetime.now()
        if not users_empty:
            for user_temp in self.cached_users:
                # remove expired record
                if user_temp.expiration_date < timestamp:
                    self.remove_users_from_cache(self.cached_users.index(user_temp))
                    break
                else:
                    continue
        if not tokens_empty:
            # clear cached tokens info
            for token_temp in self.cached_tokens:
                # remove expired record
                if token_temp.expiration_date < timestamp:
                    self.remove_tokens_from_cache(self.cached_tokens.index(token_temp))
                    break
                else:
                    continue
