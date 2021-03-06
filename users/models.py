import json

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def get_token(self):
        social = self.social_auth.get(provider='coinbase')
        return social.extra_data.get('access_token')

    def get_user_data(self):
        url = "https://api.coinbase.com/v2/user"
        response = requests.get(url, headers={
            "Authorization": f"Bearer {self.get_token()}",
            "CB-VERSION": "2016 - 09 - 15"
        })
        return json.loads(response.content)

    def get_account(self, currency):
        url = f"https://api.coinbase.com/v2/accounts/{currency}/"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.get_token()}"})
        return json.loads(response.content)['data']

    def transfer_money(self, receiver, amount, currency):
        account_id = self.get_account(currency)['id']
        url = f"https://api.coinbase.com/v2/accounts/{account_id}/transactions"
        response = requests.post(
            url,
            json={
                'type': 'send',
                'to': receiver,
                'amount': float(amount),
                'currency': currency
            },
            headers={
                "Authorization": f"Bearer {self.get_token()}",
            }
        )
        print(response.content)
        return json.loads(response.content)['data']

    def check_if_payment(self):
        labeled = self.label_set.count()
        return labeled and (labeled % settings.REWARD_AFTER == 0)

    def pay(self, amount, currency):
        admin = CustomUser.objects.get(is_superuser=True)
        admin.transfer_money(self.email, amount, currency)
