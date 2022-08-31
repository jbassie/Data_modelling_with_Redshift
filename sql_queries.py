import configparser

#CONFIG
config =configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get("S3", "LOG_DATA")
LOG_PATH = config.set('S3', "LOG_JSONPATH")
SONG_PATH = config.get("S3", "SONG_DATA")
IAM_ROLE = config.get("IAM_ROLE", "ARN")

#DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXIST staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXIST artists"

#CREATE TABLES

staging_events_table_create = """
CREATE TABLE IF NOT EXISTS staging_events(
    artist TEXT,
    auth TEXT,
    firstname TEXT,
    gender TEXT,
    itemInSession INT,
    lastname TEXT,
    length FLOAT,
    level TEXT,
    location TEXT,
    method TEXT,
    page TEXT,
    regstration TEXT,
    sessionId INT
    song TEXT,
    status INT,
    ts BIGINT,
    userAgent TEXT
    userId INT
)
"""

staging_songs_table_create ="""
CREATE TABLE IF NOT EXISTS staging_songs(
    song_id TEXT PRIMARY KEY,
    artist_id TEXT,
    artist_latitude FLOAT,
    artist_latitude FLOAT,
    artist_location TEXT,
    artist_name VARCHAR(255),
    duration FLOAT,
    num_songs INT,
    title TEXT,
    year INT
)
"""
songplay_table_create = """
CREATE TABLE IF NOT EXISTS songplays(
    songplay_id     integer identity(0,1) primary key,
    start_time      timestamp not null sortkey distkey,
    user_id         integer not null,
    level           varchar,
    song_id         varchar not null,
    artist_id       varchar not null,
    session_id      integer,
    location        varchar,
    user_agent      varchar 

)
"""

user_table_create = """
CREATE TBALE IF NOT EXISTS users(
    user_id VARCHAR PRIMARY KEY NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR
)

"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs(
    song_id     VARCHAR PRIMARY NOT NULL,
    title       VARCHAR NOT NULL,
    artist_id   VARCHAR NOT NULL,
    year        INT,
    duration FLOAT
)
"""

artist_table_create = """
CREATE TABLE IF NOT EXIST artist(
    artist_id VARCAHR PRIMARY KEY NOT NULL,
    name VARCHAR,
    location VARCHAR,
    latitude VARCHAR,
    longitude VARCAHR
)
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time(
    start_time  timestamp not null distkey sortkey primary key,
    hour    integer not null,
    day     integer not null,
    week    integer not null,
    month   integer not null,
    year    integer not null,
    weeekday   varchar not null
)
"""

#STAGING TABLES

staging_events_copy = ("""
copy staging_events from {bucket}
    credentials 'aws_iam_role = {role}'
    region      'us-west-2'
    format      as JSON {path}
    timeformat  as 'epochmillisecs'
""").format(bucket = LOG_DATA, role=IAM_ROLE, path=LOG_PATH)

staging_songs_copy = ("""
    copy staging_songs from {bucket}
    credentials 'aws_iam_role= {role}'
    region      'us-west-2'
    format      as JSON 'auto'
""").format(bucket = SONG_DATA, role=IAM_ROLE)

#FINAL TABLES

songplay_table_insert = ("""
insert into songplays (start_time, user_id, level, song_id, artist_id, location, user_agent)
    SELECT DISTINCT TIMESTAMP 'epoch' + (e.ts/ 1000) * INTERVAL '1 second' as start_time,
        e.userId    as user_id,
        e.level     as level,
        s.song_id   as  song_id,
        e.sessionId as  session_id,
        e.location  as  location,
        e.userAgent as  user_agent
    from staging_events e
    join staging_songs  s
    on e.song = s.title and e.artist  = s.artist_name and e.page = 'NextSong' and e.length = s.duration
""")

user_table_insert = ( """
insert into users(user_id, first_name, last_name, gender, level)
    select
        distinct(UserId)    as user_id
        firstname           as first_name
        lastName            as last_name
        gender,
        level
    from staging_events
    where user_id is not null
    and page = "NextSong
""")

song_table_insert = ("""
INSERT INTO songs SELECT DSITINCT (song_id)
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists SELECT DISTINCT (artist_id)
        artist_id.
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time
    WITH temp_time as (SELECT TIMESTAMP 'epoch' + (ts/1000 * INTERVAL '1 Second') as ts FROM staging_events)
    SELECT DISTINCT
    ts,
    extract(hour from ts),
    extract(day from ts),
    extract(week from ts),
    extract(month from ts),
    extract(year from ts)
    extract(weekday from ts)
    FROM temp_time
""")

#QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
