CREATE TABLE IF NOT EXISTS Mortos(
	id_morto INT NOT NULL,
	andamento_rito VARCHAR(20) NOT NULL,
	causa_morte VARCHAR(30) NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY (id_morto),
	FOREIGN KEY (user_id) REFERENCES cadastro(user_id)
)