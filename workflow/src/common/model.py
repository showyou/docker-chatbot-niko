#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, MetaData, Table, types
from datetime import datetime


class Trend(object):
    pass

init = False
#Base = declarative_base()

metadata = sqlalchemy.MetaData()

trend = Table("trend",metadata,
                Column('id', types.Integer, primary_key=True),
                Column('text', types.Text),
                Column('datetime', types.DateTime, default=datetime.now),
                mysql_engine = 'InnoDB',
                mysql_charset = 'utf8mb4'
            )


def startSession(conf):
    global init
    config = {
        "sqlalchemy.url":\
        "mysql+pymysql://"+conf["dbuser"]+":"+conf["dbpass"]+"@"+conf["dbhost"]+"/"+\
        conf["db"]+"?charset=utf8mb4",
        "sqlalchemy.echo":"False"
        }
    engine = sqlalchemy.engine_from_config(config)

    dbSession = scoped_session(
                    sessionmaker(
                        autoflush = True,
                        autocommit = False,
                        bind = engine
                    )
                )

    if init == False:
        mapper(Trend, trend)
        init = True
    metadata.create_all(bind=engine)
    print ("--start DB Session--")
    return dbSession
		
"""
# テスト内容
a = startSession()
>>> --start DB Session--
"""	
