def success_response(data=None, meta=None):
    response = {"success": True, "data": data}
    if meta:
        response["meta"] = meta
    return response

def error_response(message, status=400):
    return {"success": False, "error": message}, status
