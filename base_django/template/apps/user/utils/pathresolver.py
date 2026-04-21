def getname_reversepath(request, name):
    app_name = (
        request.resolver_match.app_name or
        request.resolver_match.namespace
    )
    if app_name != "None":
        return f'{app_name}:{name}'
    else:
        return str(name)