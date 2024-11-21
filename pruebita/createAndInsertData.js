const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  user: 'usertiktoc',
  password: 'tiktocpass',
  database: 'tiktocdb',
});

const createAndInsertData = async () => {
  try {
    // Conectar a la base de datos
    await client.connect();

    // Crear tablas
    await client.query(`
      CREATE TABLE IF NOT EXISTS Movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR NOT NULL,
        original_title VARCHAR,
        overview TEXT,
        tagline VARCHAR,
        release_date DATE,
        runtime INTEGER,
        budget DECIMAL,
        revenue DECIMAL,
        status VARCHAR,
        popularity DECIMAL,
        vote_average DECIMAL,
        vote_count INTEGER,
        poster_path VARCHAR,
        backdrop_path VARCHAR,
        homepage VARCHAR,
        imdb_id VARCHAR,
        original_language VARCHAR
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS Genres (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS Movie_Genres (
        movie_id INTEGER REFERENCES Movies(id),
        genre_id INTEGER REFERENCES Genres(id),
        PRIMARY KEY (movie_id, genre_id)
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS Movie_Cast (
        id SERIAL PRIMARY KEY,
        actor_id INTEGER,
        movie_id INTEGER REFERENCES Movies(id),
        character VARCHAR,
        cast_id INTEGER,
        credit_id VARCHAR,
        cast_order INTEGER, --cambio de nombre
        job VARCHAR
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        email VARCHAR UNIQUE,
        phone_number VARCHAR UNIQUE,
        password_hash VARCHAR,
        otp_code VARCHAR,
        otp_expiration TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        is_verified BOOLEAN DEFAULT FALSE
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS User_Profiles (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES Users(id) UNIQUE,
        username VARCHAR NOT NULL UNIQUE,
        birth_date DATE,
        country VARCHAR,
        profile_picture VARCHAR,
        gender VARCHAR CHECK (gender IN ('male', 'female', 'non-binary', 'prefer_not_to_say')),
        level VARCHAR DEFAULT 'Principiante',
        total_surveys INTEGER DEFAULT 0,
        total_coins INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS Recommendations (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER REFERENCES Movies(id)
      );
    `);

    await client.query(`
      CREATE TABLE IF NOT EXISTS Watch_Providers (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER REFERENCES Movies(id),
        country_iso CHAR(2),
        provider_id INTEGER,
        type VARCHAR CHECK (type IN ('buy', 'rent', 'flatrate', 'free')),
        display_priority INTEGER,
        link VARCHAR,
        cost INTEGER DEFAULT 0
      );
    `);

    // Insertar datos de ejemplo
     // Insertar datos en Movies
     await client.query(`
        INSERT INTO Movies (
          title, original_title, overview, tagline, release_date, runtime, 
          budget, revenue, status, popularity, vote_average, vote_count, 
          poster_path, backdrop_path, homepage, imdb_id, original_language
        ) VALUES 
          ('Movie 1', 'Original Movie 1', 'An epic story.', 'The best movie ever.', '2024-01-01', 120, 
           100000, 500000, 'Released', 7.8, 8.5, 120, '/poster1.jpg', '/backdrop1.jpg', 
           'http://movie1.com', 'tt1234567', 'en'),
          ('Movie 2', 'Original Movie 2', 'A thrilling adventure.', 'Don''t miss it.', '2024-02-01', 115, 
           200000, 750000, 'Released', 6.9, 7.0, 95, '/poster2.jpg', '/backdrop2.jpg', 
           'http://movie2.com', 'tt7654321', 'es');
      `);
      
      // Insertar datos en Genres
      await client.query(`
        INSERT INTO Genres (name) VALUES
          ('Action'),
          ('Comedy'),
          ('Drama');
      `);
  
      // Insertar datos en Movie_Genres
      await client.query(`
        INSERT INTO Movie_Genres (movie_id, genre_id) VALUES
          (1, 1), -- Movie 1 es de género Action
          (2, 2), -- Movie 2 es de género Comedy
          (2, 3); -- Movie 2 también es de género Drama
      `);
  
      // Insertar datos en Movie_Cast
      await client.query(`
        INSERT INTO Movie_Cast (actor_id, movie_id, character, cast_id, credit_id, cast_order, job) VALUES
          (101, 1, 'Hero', 1, 'credit_001', 1, 'Actor'),
          (102, 1, 'Villain', 2, 'credit_002', 2, 'Actor'),
          (103, 2, 'Sidekick', 3, 'credit_003', 1, 'Actor');
      `);
  
      // Insertar datos en Users
      await client.query(`
        INSERT INTO Users (email, phone_number, password_hash, otp_code, otp_expiration) VALUES
          ('user1@example.com', '1234567890', 'hashed_password_1', 'OTP123', '2024-11-30 23:59:59'),
          ('user2@example.com', '0987654321', 'hashed_password_2', 'OTP456', '2024-12-01 23:59:59');
      `);
  
      // Insertar datos en User_Profiles
      await client.query(`
        INSERT INTO User_Profiles (user_id, username, birth_date, country, profile_picture, gender, level, total_surveys, total_coins) VALUES
          (1, 'UserOne', '2000-01-01', 'US', '/profile1.jpg', 'male', 'Intermediate', 10, 500),
          (2, 'UserTwo', '1995-06-15', 'MX', '/profile2.jpg', 'female', 'Advanced', 20, 1000);
      `);
  
      // Insertar datos en Recommendations
      await client.query(`
        INSERT INTO Recommendations (movie_id) VALUES
          (1),
          (2);
      `);
  
      // Insertar datos en Watch_Providers
      await client.query(`
        INSERT INTO Watch_Providers (movie_id, country_iso, provider_id, type, display_priority, link, cost) VALUES
          (1, 'US', 101, 'rent', 1, 'http://provider1.com/movie1', 5),
          (2, 'MX', 102, 'buy', 1, 'http://provider2.com/movie2', 10);
      `);
  
      console.log("Datos de ejemplo insertados correctamente.");
    } catch (err) {
      console.error("Error al insertar los datos de ejemplo:", err);
    } finally {
      await client.end();
    }
  };
  

createAndInsertData();
