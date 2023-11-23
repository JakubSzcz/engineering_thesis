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


class GetResponses(BaseModel):
    message: str = Field(title="Message information", examples=["Record successfully retrieved"],
                         default="Records successfully retrieved")
    db_type: str = Field(title="Database type", examples=["PSQL"])
    title_basics: list | None = Field(title="Title Basics response", default=None)
    title_episodes: list | None = Field(title="Title Episodes response", default=None)
    name_basics: list | None = Field(title="Name Basics response", default=None)


class GetTableResponses(BaseModel):
    message: str = Field(title="Message information", examples=["Records from table {table_name} "
                                                                "successfully retrieved"],
                         default="Records successfully retrieved")
    db_type: str = Field(title="Database type", examples=["PSQL"])
    table_name: str = Field(title="Table name", description="Data retrieved from specified table",
                            examples=["title_basics"])
    data: list[dict] | None = Field(title="Title Basics response", default=None)


class GetRecordResponses(BaseModel):
    message: str = Field(title="Message information", examples=["The record data from table {table_name} "
                                                                "successfully retrieved"],
                         default="Record successfully retrieved")
    db_type: str = Field(title="Database type", examples=["PSQL"])
    table_name: str = Field(title="Table name", description="Data retrieved from specified table",
                            examples=["title_basics"])
    record_id: str = Field(title="Record identifier", description="Identifies specific record in table",
                           example="tt0000004")
    data: dict = Field(title="Data response")


class UpdateTitleBasic(BaseModel):
    titleType: str | None = Field(title="Title type", examples=["short"], default=None)
    primaryTitle: str | None = Field(title="Primary Title", examples=["The Photographical Congress Arrives in Lyon"],
                                     default=None)
    originalTitle: str | None = Field(title="Original Title", examples=["Le débarquement du congrès de photographie"
                                                                        " à Lyon"], default=None)
    isAdult: int | None = Field(title="Is Adult", examples=[0], default=None)
    startYear: int | None = Field(title="Start Year", examples=[1895])
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
    db_type: str = Field(title="Database type", examples=["PSQL"])
    table_name: str = Field(title="Table name", description="Data retrieved from specified table",
                            examples=["title_basics"])
    old_data: dict = Field(title="Old data response", description="Old data details")
    new_data: dict = Field(title="New data response", description="New data details")


queries_list_info = {
    "query_1":
        {
            "description": "Find the average age of actors/actresses (primaryProfession = 'actor' or 'actress')"
                           " for titles that are of type 'movie' and have a runtime greater than 120 minutes.",
            "tables_involved": ["title_basics", "name_basics"]
         },
    "query_2":
        {
            "description": "Find top 10 tvSeries based on theirs season number, where start year is greater than 2000",
            "tables_involved": ["title_basics", "title_episodes"]
        }
}

