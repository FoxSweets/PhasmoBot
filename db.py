import sqlite3

with sqlite3.connect("database.db") as db:
	cursor = db.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS "bots_games" (
		"server_id_bg"	INT,
		"games"	INT,
		"Ghost"	INT,
		"age"	INT,
		"level"	INT,
		"agr"	INT,
		"max_agr"	INT,
		"agr_level"	INT,
		"players"	INT,
		"salt_g"	INT,
		"cross_g"	INT,
		"sen1_g"	INT,
		"sen2_g"	INT,
		"torch_g"	INT,
		"camera_g"	INT,
		"item1_g"	INT,
		"item2_g"	INT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS "rank" (
		"id_rank"	INT,
		"name_rank"	TEXT,
		"win_min"	INT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS "update" (
		"id_up"	REAL,
		"name_up"	TEXT,
		"date_up"	BLOB
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS "profile" (
		"server_id_p"	INT,
		"action_on_p"	INT,
		"id_p"	INT,
		"nick_p"	TEXT,
		"update_p"	REAL,
		"rank_p"	INT,
		"win_p"	INT,
		"lose_p"	INT,
		"money_p"	INT,
		"salt_p"	INT,
		"cross_p"	INT,
		"mw_1_p"	INT,
		"mw_2_p"	INT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS "shop" (
		"id_item"	INT,
		"name_item"	TEXT,
		"disc_item"	TEXT,
		"give_money"	INT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS "ghosts" (
		"ghost_id"	INT,
		"name"	TEXT,
		"song"	INT,
		"item_home"	INT,
		"el_item_home"	INT,
		"sen1_item"	INT,
		"sen2_item"	INT,
		"torch_item"	INT,
		"camera_item"	INT,
		"item1_home"	INT,
		"item2_home"	INT
	)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
		"server_id"	INT,
		"id"	INT,
		"nickname"	TEXT,
		"activ_game"	INT,
		"player"	INT,
		"use_one"	INT,
		"salt"	INT,
		"cross"	INT,
		"sen1"	INT,
		"sen2"	INT,
		"camera"	INT,
		"item1"	INT,
		"item2"	INT,
		"torch"	INT,
		"mw_1"	INT,
		"mw_2"	INT
	)""")