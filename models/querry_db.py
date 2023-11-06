from pydantic import BaseModel, Field
from typing import List


class InsertTitleBasic(BaseModel):
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: int
    startYear: int
    endYear: int
    runtimeMinutes: int
    genres: str


class InsertNameBasic(BaseModel):
    nconst : str
    primaryName: str
    birthYear: int
    deathYear: int
    primaryProfession: List[str]
    knownForTitles: List[str]


class InsertTitleEpisode(BaseModel):
    tconst: str
    parentTconst: str
    seasonNumber: int
    episodeNumber: int
