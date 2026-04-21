from allauth.account.adapter import DefaultAccountAdapter
from apps.user.auth import flow_fix
from allauth.core import context

class CustomAccountAdapter(DefaultAccountAdapter):
    
    def get_reset_password_from_key_url(self, key):
        return flow_fix.get_reset_password_from_key_url(self.request, key)

    


