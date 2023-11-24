# contains models of responses/requests connected with data related operations and additional
# information required for data processing

# imports
from pydantic import BaseModel, Field


# REQUEST
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


class InsertNameBasic(BaseModel):
    nconst: str = Field(title="Name Basic Primary Key", examples=["nm0000001"])
    primaryName: str = Field(title="Primary Name", examples=["Richard Burton"])
    birthYear: int = Field(title="Birth Year", examples=[1925])
    deathYear: int = Field(title="Death Year", examples=[1984], description="If equals to '-1'; still alive")
    # coma separated list
    primaryProfession: str = Field(title="Primary Profession", examples=["actor,soundtrack,producer"])
    knownForTitles: str = Field(title="Known For Titles", examples=["tt0057877,tt0087803,tt0061184,tt0059749"])


class InsertTitleEpisode(BaseModel):
    tconst: str = Field(title="Title Episode Primary Key", examples=["tt0000001"])
    parentTconst: str = Field(title="Parent Title Episode/Basic Primary Key", examples=["tt0000001"])
    seasonNumber: int = Field(title="Season Number", examples=[2])
    episodeNumber: int = Field(title="Episode Number", examples=[16])


# OTHERS
redis_models_fields_tuple = {
    "title_basics": ("@tconst", "@titleType", "@primaryTitle", "@originalTitle", "@isAdult", "@startYear",
                     "@endYear", "@runtimeMinutes", "@genres"),
    "name_basics": ("@nconst", "@primaryName", "@birthYear", "@deathYear", "@primaryProfession",
                    "@knownForTitles"),
    "title_episodes": ("@tconst", "@parentTconst", "@seasonNumber", "@episodeNumber")
}

queries_list_info = {
    "query_1":
        {
            "description": "Find the average age of actors/actresses (primaryProfession = 'actor' or 'actress')"
                           " for titles that are of type 'movie' and have a runtime greater than 120 minutes.",
            "tables_involved": ["title_basics", "name_basics"]
         },
    "query_2":
        {
            "description": "Find top 10 tvSeries based on theirs season number",
            "tables_involved": ["title_basics", "title_episodes"]
        }
}

queries = {
    "psql": [
        "SELECT AVG(CASE WHEN deathYear = -1 THEN 2023 - birthYear ELSE deathYear - birthYear END) FROM "
        "(SELECT DISTINCT nconst, birthYear, deathYear FROM title_basics AS tb JOIN name_basics AS nb ON "
        "tb.tconst = ANY(nb.knownForTitles) WHERE tb.titleType = 'movie' AND tb.runtimeMinutes > 120 AND "
        "('actor' = ANY(nb.primaryProfession) OR 'actress' = ANY(nb.primaryProfession)) AND nb.birthYear != -1);",

        "SELECT primaryTitle, te3.seasons AS seasons_number, startYear FROM title_basics JOIN "
        "(SELECT te2.parenttconst, MAX(te1.seasonnumber) AS seasons FROM title_episodes AS te1 JOIN "
        "(SELECT DISTINCT parenttconst FROM title_episodes) AS te2 ON te2.parenttconst = te1.parenttconst "
        "WHERE te1.seasonnumber < 800 GROUP BY te2.parenttconst) AS te3 ON tconst = te3.parenttconst "
        "WHERE startYear >= 2000 ORDER BY seasons_number DESC LIMIT 10;"
    ],
    "redis": [],
    "mdb": [
        [{"$match": {"titleType": "movie", "runtimeMinutes": {"$gt": 120}}}, {"$lookup": {"from": "name_basics",
        "localField": "tconst", "foreignField": "knownForTitles", "as": "name_basics"}}, {"$unwind": "$name_basics"},
        {"$match": {"$or": [{"name_basics.primaryProfession": "actor"}, {"name_basics.primaryProfession": "actress"}],
        "name_basics.birthYear": {"$ne": -1}}}, {"$group": {"_id": "$name_basics.nconst", "avgAge": {"$avg": {"$cond":
        {"if": {"$eq": ["$name_basics.deathYear", -1]}, "then": {"$subtract": [2023, "$name_basics.birthYear"]},
        "else": {"$subtract": ["$name_basics.deathYear", "$name_basics.birthYear"]}}}}}},
        {"$group": {"_id": None, "avgAge": {"$avg": "$avgAge"}, "count": {"$sum": 1}}}],

        [{"$match": {"startYear": {"$gte": 2000}, "titleType": "tvSeries"}}, {"$lookup": {"from": "title_episodes",
        "localField": "tconst", "foreignField": "parentTconst", "as": "episodes"}}, {"$unwind": "$episodes"},
        {"$match": {"episodes.seasonNumber": {"$lt": 800}}}, {"$group": {"_id": "$tconst", "seasons": {"$max":
        "$episodes.seasonNumber"}, "primaryTitle": {"$first": "$primaryTitle"}, "startYear": {"$first": "$startYear"}}},
        {"$sort": {"seasons": -1}}, {"$limit": 10},
        {"$project": {"_id": 0, "primaryTitle": 1, "seasons_number": "$seasons", "startYear": 1}}]
    ],
    "sqlite": [
        "SELECT COUNT(*) FROM "
        "(SELECT DISTINCT nconst, birthYear, deathYear FROM title_basics AS tb JOIN name_basics AS nb ON "
        "tb.tconst = nb.knownForTitles WHERE tb.titleType = 'movie' AND tb.runtimeMinutes > 120 AND "
        "('actor' = nb.primaryProfession OR 'actress' = nb.primaryProfession) AND nb.birthYear != -1);",

        "SELECT primaryTitle, te3.seasons AS seasons_number, startYear FROM title_basics JOIN "
        "(SELECT te2.parenttconst, MAX(te1.seasonnumber) AS seasons FROM title_episodes AS te1 JOIN "
        "(SELECT DISTINCT parenttconst FROM title_episodes) AS te2 ON te2.parenttconst = te1.parenttconst "
        "WHERE te1.seasonnumber < 800 GROUP BY te2.parenttconst) AS te3 ON title_basics.tconst = te3.parenttconst "
        "WHERE startYear >= 2000 ORDER BY seasons_number DESC LIMIT 10;"
    ]
}
