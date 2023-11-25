# contains models of responses/requests connected with data related operations and additional
# information required for data processing

# libraries imports
from pydantic import BaseModel, Field


# REQUEST
class InsertTitleBasic(BaseModel):
    tconst: str = Field(title="Title identifier", example="tt0061184")
    titleType: str = Field(title="Title type", examples=["short"])
    primaryTitle: str = Field(title="Primary Title", examples=["The Photographical Congress Arrives in Lyon"])
    originalTitle: str = Field(title="Original Title", examples=["Le débarquement du congrès de photographieà Lyon"])
    isAdult: int = Field(title="Is Adult", examples=[0])
    startYear: int = Field(title="Start Year", examples=[1895])
    endYear: int = Field(title="End Year", examples=[1898], description="If equals to '-1'; field not provided")
    runtimeMinutes: int = Field(title="Runtime Minutes", examples=[45], description="If equals to '-1'; "
                                                                                    "field not provided")
    genres: str = Field(title="Primary Title", examples=["Romance"])


class InsertNameBasic(BaseModel):
    nconst: str = Field(title="Name identifier", example="nm0005251")
    primaryName: str = Field(title="Primary Name", examples=["Richard Burton"])
    birthYear: int = Field(title="Birth Year", examples=[1925])
    deathYear: int = Field(title="Death Year", examples=[1984], description="If equals to '-1'; still alive")
    # coma separated list:
    primaryProfession: str = Field(title="Primary Profession", examples=["actor,soundtrack,producer"])
    knownForTitles: str = Field(title="Known For Titles", examples=["tt0057877,tt0087803,tt0061184,tt0059749"])


class InsertTitleEpisode(BaseModel):
    tconst: str = Field(title="Title identifier", example="tt0059749")
    parentTconst: str = Field(title="Parent Title Episode/Basic Primary Key", examples=["tt0000001"])
    seasonNumber: int = Field(title="Season Number", examples=[2])
    episodeNumber: int = Field(title="Episode Number", examples=[16])


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


class UpdateTitleEpisode(BaseModel):
    parentTconst: str | None = Field(title="Parent Title Episode/Basic Primary Key", examples=["tt0000001"],
                                     default=None)
    seasonNumber: int | None = Field(title="Season Number", examples=[2], default=None)
    episodeNumber: int | None = Field(title="Episode Number", examples=[16], default=None)


# RESPONSE
class PatchRecordResponses(BaseModel):
    message: str = Field(title="Message information", examples=["The record data from table {table_name} "
                                                                "successfully updated"],
                         default="Record successfully updated")
    old_data: dict = Field(title="Old data response", description="Old data details")
    new_data: dict = Field(title="New data response", description="New data details")
