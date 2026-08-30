from typing import NamedTuple

class CreateAccount(NamedTuple):
    username: str
    userid: str
    mr_id: str
    
class UpdateProfile(NamedTuple):
    name: str
    description: str
    image: str
    follower: int
    follow: int
    user_name: str