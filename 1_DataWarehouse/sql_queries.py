import configparser
# timestamp 'epoch' + CAST(e.ts AS BIGINT)/1000 * interval '1 second' END 

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

DWH_ROLE_ARN = config.get("IAM_ROLE","ARN")
LOG_DATA = config.get("S3","LOG_DATA")
LOG_DATA_DSND = config.get("S3","LOG_DATA_DSND")
LOG_DATA_MINI = config.get("S3","LOG_DATA_MINI")
SONG_DATA = config.get("S3","SONG_DATA")
LOG_PATH = config.get("S3","LOG_JSONPATH")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
staging_events_dsnd_table_drop = "DROP TABLE IF EXISTS staging_events_dsnd"
staging_events_mini_table_drop = "DROP TABLE IF EXISTS staging_events_mini"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""  CREATE TABLE IF NOT EXISTS staging_events
                                            (
                                                artist          VARCHAR,
                                                auth            VARCHAR, 
                                                firstName       VARCHAR,
                                                gender          VARCHAR,   
                                                itemInSession   INTEGER,
                                                lastName        VARCHAR,
                                                length          FLOAT,
                                                level           VARCHAR, 
                                                location        VARCHAR,
                                                method          VARCHAR,
                                                page            VARCHAR,
                                                registration    TIMESTAMP,
                                                sessionId       INTEGER,
                                                song            VARCHAR,
                                                status          INTEGER,
                                                ts              TIMESTAMP,
                                                userAgent       VARCHAR,
                                                userId          INTEGER
                                            ); """)

staging_events_dsnd_table_create= ("""  CREATE TABLE IF NOT EXISTS staging_events_dsnd
                                            (
                                                status          INTEGER,
                                                gender          VARCHAR,   
                                                length          FLOAT,
                                                firstName       VARCHAR,
                                                level           VARCHAR, 
                                                lastName        VARCHAR,
                                                registration    VARCHAR,
                                                userId          VARCHAR,
                                                ts              VARCHAR,
                                                auth            VARCHAR, 
                                                page            VARCHAR,
                                                sessionId       INTEGER,
                                                location        VARCHAR,
                                                itemInSession   INTEGER,
                                                userAgent       VARCHAR,
                                                song            VARCHAR,
                                                artist          VARCHAR,
                                                method          VARCHAR
                                            ); """)

staging_events_mini_table_create = """CREATE TABLE IF NOT EXISTS staging_events_mini
                                            (
                                                ts              VARCHAR,
                                                userId          VARCHAR,
                                                sessionId       INTEGER,
                                                page            VARCHAR,
                                                auth            VARCHAR, 
                                                method          VARCHAR,
                                                status          INTEGER,
                                                level           VARCHAR, 
                                                itemInSession   INTEGER,
                                                location        VARCHAR,
                                                userAgent       VARCHAR,
                                                lastName        VARCHAR,
                                                firstName       VARCHAR,
                                                registration    VARCHAR,
                                                gender          VARCHAR, 
                                                artist          VARCHAR,                                                
                                                song            VARCHAR,                                                
                                                length          FLOAT                                            
                                            ); """

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS staging_songs
                                            (
                                              num_song          INTEGER,
                                              artist_id         VARCHAR,
                                              artist_latitude   FLOAT,
                                              artist_longitude  FLOAT,
                                              artist_location   VARCHAR,
                                              artist_name       VARCHAR,
                                              song_id           VARCHAR,
                                              title             VARCHAR,
                                              duration          FLOAT,
                                              year              INTEGER
                                            ); """)

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays
                                            (
                                              songplay_id       INTEGER IDENTITY(0,1) PRIMARY KEY sortkey,
                                              start_time        TIMESTAMP,
                                              user_id           INTEGER,
                                              level             VARCHAR, 
                                              song_id           VARCHAR,
                                              artist_id         VARCHAR,
                                              session_id        INTEGER,
                                              location          VARCHAR,
                                              user_agent        VARCHAR,
                                              itemInSession     INTEGER,
                                              status            INTEGER,
                                              page              VARCHAR,
                                              method            VARCHAR,
                                              auth              VARCHAR
                                            ); """)


user_table_create = ("""CREATE TABLE IF NOT EXISTS users
                                            (
                                              user_id           INTEGER  PRIMARY KEY,
                                              first_name        VARCHAR, 
                                              last_name         VARCHAR, 
                                              gender            VARCHAR, 
                                              level             VARCHAR,
                                              registration      TIMESTAMP
                                            ); """)

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs
                                            (
                                              song_id           VARCHAR  PRIMARY KEY,
                                              title             VARCHAR, 
                                              artist_id         VARCHAR,
                                              year              INTEGER,
                                              duration          FLOAT
                                            ); """)


artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                                            (
                                              artist_id         VARCHAR  PRIMARY KEY,
                                              name              VARCHAR, 
                                              location          VARCHAR, 
                                              lattitude         FLOAT,
                                              longitude         FLOAT
                                            ); """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
                                            (
                                              start_time        TIMESTAMP  PRIMARY KEY,
                                              hour              INTEGER,
                                              day               INTEGER,
                                              week              INTEGER, 
                                              month             INTEGER,
                                              year              INTEGER,
                                              weekday           INTEGER   
                                              );""")

# STAGING TABLES

staging_events_copy = ("""  COPY staging_events FROM {}
                            CREDENTIALS 'aws_iam_role={}'
                            COMPUPDATE OFF region 'us-west-2'
                            TIMEFORMAT as 'epochmillisecs'
                            TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
                            FORMAT AS JSON {};
                            """).format(LOG_DATA,DWH_ROLE_ARN,LOG_PATH)

staging_songs_copy = ("""   COPY staging_songs FROM {}
                            CREDENTIALS 'aws_iam_role={}'
                            COMPUPDATE OFF region 'us-west-2'
                            FORMAT AS JSON 'auto' 
                            TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
                            """).format(SONG_DATA,DWH_ROLE_ARN)

staging_events_dsnd_copy = ("""   COPY staging_events_dsnd FROM {}
                            CREDENTIALS 'aws_iam_role={}'
                            COMPUPDATE OFF region 'us-west-2'
                            FORMAT AS JSON 'auto' 
                            TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
                            """).format(LOG_DATA_DSND,DWH_ROLE_ARN)   

staging_events_mini_copy = ("""   COPY staging_events_mini FROM {}
                            CREDENTIALS 'aws_iam_role={}'
                            COMPUPDATE OFF region 'us-west-2'
                            FORMAT AS JSON 'auto' 
                            TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
                            """).format(LOG_DATA_MINI,DWH_ROLE_ARN)                                                       

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays(start_time,
                                                  user_id,
                                                  level, 
                                                  song_id,
                                                  artist_id,
                                                  session_id,
                                                  location,
                                                  user_agent,
                                                  itemInSession,
                                                  status,
                                                  page,
                                                  method,
                                                  auth)
                            SELECT DISTINCT
                                              e.ts as start_time,
                                              e.userId as user_id,
                                              e.level as level,
                                              s.song_id as song_id,
                                              s.artist_id as artist_id,
                                              e.sessionId as session_id,
                                              s.artist_location as location,
                                              e.useragent as user_agent,
                                              e.itemInSession,
                                              e.status,
                                              e.page,
                                              e.method,
                                              e.auth
                                 FROM staging_events e
                                 LEFT JOIN staging_songs s
                                 ON e.artist = s.artist_name AND e.song = s.title
                               """)


user_table_insert = ("""INSERT INTO users(user_id,
                                         first_name, 
                                         last_name, 
                                         gender, 
                                         level,
                                         registration)
                        SELECT DISTINCT userId,
                                        firstName,
                                        lastName,
                                        gender,
                                        level,
                                        registration
                        FROM staging_events e
                        WHERE userId IS NOT NULL; """)


song_table_insert = ("""INSERT INTO songs (song_id,
                                          title, 
                                          artist_id,
                                          year,
                                          duration)
                        SELECT DISTINCT song_id,
                                        title,
                                        artist_id,
                                        year,
                                        duration
                        FROM staging_songs
                        WHERE song_id IS NOT NULL; """)

artist_table_insert = ("""INSERT INTO artists (artist_id,
                                              name, 
                                              location, 
                                              lattitude,
                                              longitude)
                            SELECT DISTINCT artist_id,
                                           artist_name,
                                           artist_location,
                                           artist_latitude,
                                           artist_longitude
                            FROM staging_songs
                            WHERE artist_id IS NOT NULL; """)

time_table_insert = ("""INSERT INTO time (start_time,
                                          hour,
                                          day,
                                          week,
                                          month,
                                          year,
                                          weekday)
                        SELECT DISTINCT e.ts,
                                            EXTRACT(hour from e.ts),
                                            EXTRACT(day from e.ts),
                                            EXTRACT(week from e.ts),
                                            EXTRACT(month from e.ts),
                                            EXTRACT(year from e.ts),
                                            EXTRACT(weekday from e.ts)
                        FROM 
                         staging_events e
                        WHERE e.ts IS NOT NULL; """)




# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_events_dsnd_table_create,  staging_events_mini_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_events_dsnd_table_drop, staging_events_mini_table_drop, staging_songs_table_drop,songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy,staging_events_dsnd_copy, staging_events_mini_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]