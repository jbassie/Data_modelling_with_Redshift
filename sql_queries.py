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
""").format(bucket - LOG_DATA, role=IAM_ROLE, path=LOG_PATH)