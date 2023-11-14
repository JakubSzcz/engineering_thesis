from pydantic import BaseModel, Field


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


class UpdateTitleBasic(BaseModel):
    titleType: str | None = Field(title="Title type", examples=["short"], default=None)
    primaryTitle: str | None = Field(title="Primary Title", examples=["The Photographical Congress Arrives in Lyon"],
                                     default=None)
    originalTitle: str | None = Field(title="Original Title", examples=["Le débarquement du congrès de photographie"
                                                                        " à Lyon"], default=None)
    isAdult: int | None = Field(title="Is Adult", examples=[0], default=None)
    startYear: int | None = Field(title="Start Year", examples=[1895], default=None)
    endYear: int | None = Field(title="End Year", examples=[1898], description="If equals to '-1'; field not provided",
                                default=None)
    runtimeMinutes: int | None = Field(title="Runtime Minutes", examples=[45],
                                       description="If equals to '-1'; field not provided", default=None)
    genres: str | None = Field(title="Primary Title", examples=["Romance"], default=None)


# model of request body to insert name_basic
class UpdateNameBasic(BaseModel):
    primaryName: str | None = Field(title="Primary Name", examples=["Richard Burton"], default=None)
    birthYear: int | None = Field(title="Birth Year", examples=[1925], default=None)
    deathYear: int | None = Field(title="Death Year", examples=[1984], description="If equals to '-1'; still alive",
                                  default=None)
    # coma separated list
    primaryProfession: str | None = Field(title="Primary Profession", examples=["actor,soundtrack,producer"],
                                          default=None)
    knownForTitles: str | None = Field(title="Known For Titles", examples=["tt0057877,tt0087803,tt0061184,tt0059749"],
                                       default=None)


# model of request body to insert title_episode
class UpdateTitleEpisode(BaseModel):
    parentTconst: str | None = Field(title="Parent Title Episode/Basic Primary Key", examples=["tt0000001"],
                                     default=None)
    seasonNumber: int | None = Field(title="Season Number", examples=[2], default=None)
    episodeNumber: int | None = Field(title="Episode Number", examples=[16], default=None)


class PatchRecordResponses(BaseModel):
    message: str = Field(title="Message information", examples=["The record data from table {table_name} "
                                                                "successfully updated"],
                         default="Record successfully updated")
    old_data: dict = Field(title="Old data response", description="Old data details")
    new_data: dict = Field(title="New data response", description="New data details")
