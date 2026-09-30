from __future__ import annotations
from datetime import datetime , timedelta
from dataclasses import dataclass

Default_expire_time = 7
Default_max_clicks = 10

class link_expired(Exception):
    pass

class click_limit_reached(Exception):
    pass

class link_not_found(Exception):
    pass

@dataclass
class link:
    token : str
    saved_filename : str
    original_filename :str
    expire_at : datetime
    max_clicks : int 
    click_count : int 

    @classmethod
    def create(cls, token :str , saved_filename : str , original_filename : str):
        return cls(
            token = token,
            saved_filename = saved_filename,
            original_filename = original_filename,
            expire_at = datetime.now() + timedelta(days=Default_expire_time),
            max_clicks = Default_max_clicks,
            click_count = 0,
        )
    
    def check_downloadable(self):
        if datetime.now() > self.expire_at :
            raise link_expired(self.token)
        if self.click_count >= self.max_clicks :
            raise click_limit_reached(self.token)

    def register_click(self):
        self.click_count += 1