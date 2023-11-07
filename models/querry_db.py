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
    nconst: str
    primaryName: str
    birthYear: int
    deathYear: int
    primaryProfession: str  # coma separated list
    knownForTitles: str  # coma separated list


class InsertTitleEpisode(BaseModel):
    tconst: str
    parentTconst: str
    seasonNumber: int
    episodeNumber: int
