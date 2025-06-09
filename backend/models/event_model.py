def validate_event(data):
    required_fields = ["name", "location", "date", "type"]
    for field in required_fields:
        if field not in data:
            return False, f"{field} is missing"
    return True, "OK"
