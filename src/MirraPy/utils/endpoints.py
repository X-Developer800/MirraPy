BASE_URL = "https://www.mirrativ.com"

class EndPoint:
    class User:
        ME = f"{BASE_URL}/api/user/me"
        PROFILE_EDIT = f"{BASE_URL}/api/user/profile_edit"
        PROFILE = f"{BASE_URL}/api/user/profile"
        LIVE_REQUEST = f"{BASE_URL}/api/user/post_live_request"
        SEARCH = f"{BASE_URL}/api/user/search"
    
    class Live:
        LIVE = f"{BASE_URL}/api/live/live"
        LIVE_HISTORY = f"{BASE_URL}/api/live/live_history"
        LIVE_POLLING = f"{BASE_URL}/api/live/live_polling"
        LEAVE = f"{BASE_URL}/api/live/leave"
        
    class Collab:
        REQUEST = f"{BASE_URL}/api/collab/request"
        CANCEL = f"{BASE_URL}/api/collab/cancel"