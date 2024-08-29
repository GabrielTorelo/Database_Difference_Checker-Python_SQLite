from constants import TRACKING_CODE

def get_ok_response() -> dict:
    return {
        "trackingCode": f"{TRACKING_CODE}.00",
        "message": "Finished successfully",
    }
