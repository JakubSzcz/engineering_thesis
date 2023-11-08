from pydantic import BaseModel, Field


# model of request body to insert title_basic
class InsertTitleBasic(BaseModel):
    tconst: str = Field(title="Title Basic Primary Key", examples=["tt0000001"])
    titleType: str = Field(title="Title type", examples=["short"])
    primaryTitle: str = Field(title="Primary Title", examples=["The Photographical Congress Arrives in Lyon"])
    originalTitle: str = Field(title="Original Title", examples=["Le débarquement du congrès de photographie à Lyon"])
    isAdult: int = Field(title="Is Adult", examples=[0])
    startYear: int = Field(title="Start Year", examples=[1895])
    endYear: int = Field(title="End Year", examples=[1898], description="If equals to '-1'; field not provided")
    runtimeMinutes: int = Field(title="Runtime Minutes", examples=[45],
                                description="If equals to '-1'; field not provided")
    genres: str = Field(title="Primary Title", examples=["Romance"])


# model of request body to insert name_basic
class InsertNameBasic(BaseModel):
    nconst: str = Field(title="Name Basic Primary Key", examples=["nm0000001"])
    primaryName: str = Field(title="Primary Name", examples=["Richard Burton"])
    birthYear: int = Field(title="Birth Year", examples=[1925])
    deathYear: int = Field(title="Death Year", examples=[1984], description="If equals to '-1'; still alive")
    # coma separated list
    primaryProfession: str = Field(title="Primary Profession", examples=["actor,soundtrack,producer"])
    knownForTitles: str = Field(title="Known For Titles", examples=["tt0057877,tt0087803,tt0061184,tt0059749"])


# model of request body to insert title_episode
class InsertTitleEpisode(BaseModel):
    tconst: str = Field(title="Title Episode Primary Key", examples=["tt0000001"])
    parentTconst: str = Field(title="Parent Title Episode/Basic Primary Key", examples=["tt0000001"])
    seasonNumber: int = Field(title="Season Number", examples=[2])
    episodeNumber: int = Field(title="Episode Number", examples=[16])


# RESPONSES
class InsertResponses(BaseModel):
    message: str = Field(title="Message information", examples=["Record successfully inserted"],
                         default="Record successfully inserted")
    db_type: str = Field(title="Database type", examples=["PSQL"])
    correlation_id: str = Field(title="Correlation_id",
                                examples=["tb:tt0000004te:tt0043426nb:nm0000004ts:1699378899tf:9903"])
    insertion_time: str = Field(title="Insertion Time", examples=["0:00:02.243829"])


class DeleteResponses(BaseModel):
    message: str = Field(title="Message information", examples=["Record successfully deleted"],
                         default="Record successfully deleted")
    db_type: str = Field(title="Database type", examples=["PSQL"])
    table_name: str = Field(title="Table name", examples=["title_basics"])
    record_id: str = Field(title="Record ID", examples=["tt0000001"])
