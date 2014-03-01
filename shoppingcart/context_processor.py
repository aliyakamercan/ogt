def add_store(request):
    if request.store:
        return {
            'store': request.store,
        }
    return {}