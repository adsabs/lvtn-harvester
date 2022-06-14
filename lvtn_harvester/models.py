import json

from lvtn1_utils import UTCDateTime, get_date
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    meta = Column(Text)  # JSON with connection info (user, password, etc...)

    def __str__(self):
        return json.dumps(self.toJSON(clean=True))

    def toJSON(self, clean=False):
        """Returns value formatted as python dict."""
        return {"id": self.id, "name": self.name, "meta": self._clean(self.meta, clean)}

    def _clean(self, item):
        if not item:
            return {}
        out = {}
        for k, v in item.items():
            if "pass" in k:
                out[k] = "***"
            else:
                out[k] = v
        return out


class Seed(Base):
    __tablename__ = "seeds"
    id = Column(Integer, primary_key=True)
    fingerprint = Column(String(255), unique=True)
    created = Column(UTCDateTime, default=get_date)
    last_accessed = Column(UTCDateTime, default=get_date)
    url = Column(String(255))
    provider = Column(Integer, ForeignKey("providers.pid"))

    def toJSON(self):
        """Returns value formatted as python dict."""
        return {
            "id": self.id,
            "fingerprint": self.fingerprint,
            "url": self.url,
            "provider": self.provider.toJSON(clean=True),
            "created": self.created and get_date(self.created).isoformat() or None,
            "last_accessed": self.last_accessed
            and get_date(self.last_accessed).isoformat()
            or None,
        }


class Fruit(Base):
    __tablename__ = "fruits"
    id = Column(Integer, primary_key=True)
    fingerprint = Column(String(255), unique=True)
    seed = Column(ForeignKey("seeds.id"))

    created = Column(UTCDateTime, default=get_date)
    last_accessed = Column(UTCDateTime, default=get_date)

    payload = Column(Text)

    def toJSON(self):
        """Returns value formatted as python dict."""
        return {
            "id": self.id,
            "fingerprint": self.fingerprint,
            "seed": self.seed.toJSON(),
            "created": self.created and get_date(self.created).isoformat() or None,
            "last_accessed": self.last_accessed
            and get_date(self.last_accessed).isoformat()
            or None,
        }
