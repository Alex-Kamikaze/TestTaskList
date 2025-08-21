from sqlalchemy.orm import Session

class Service:
    
    def __init__(self, session: Session):
        self.session = session