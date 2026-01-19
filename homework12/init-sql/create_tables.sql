CREATE TABLE IF NOT EXISTS model_performance(
    training_date DATE NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    training_set_size INT NOT NULL,
    mae FLOAT NOT NULL
);