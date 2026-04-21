from django.http import JsonResponse

def get_provider_url(user):
    social = user.socialaccount_set.first()
    
    if not social:
        return
    data = social.extra_data
    match social.provider:
        case "google":
            return data.get("picture")
        case "facebook":
            return data.get("picture", {}).get("data", {}).get("url")
        case _:
            print("Provider is not available")
            return
     

    
