const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  user: 'usertiktoc',
  password: 'tiktocpass',
  database: 'tiktocdb',
});

const verifyTablesAndData = async () => {
    try {
      // Conectar a la base de datos
      await client.connect();
  
      // Verificar si las tablas existen
      const tablesResult = await client.query(`
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
      `);
      console.log("Tablas en la base de datos:");
      tablesResult.rows.forEach(table => {
        console.log(`- ${table.table_name}`);
      });
  
      // Verificar los registros en la tabla Movies
      const moviesResult = await client.query(`
        SELECT * FROM Movies;
      `);
      console.log("\nDatos en la tabla Movies:");
      console.table(moviesResult.rows);
  
      // Verificar los registros en la tabla Genres
      const genresResult = await client.query(`
        SELECT * FROM Genres;
      `);
      console.log("\nDatos en la tabla Genres:");
      console.table(genresResult.rows);
  
      // Verificar los registros en la tabla Movie_Genres
      const movieGenresResult = await client.query(`
        SELECT * FROM Movie_Genres;
      `);
      console.log("\nDatos en la tabla Movie_Genres:");
      console.table(movieGenresResult.rows);
  
      // Verificar los registros en la tabla Movie_Cast
      const movieCastResult = await client.query(`
        SELECT * FROM Movie_Cast;
      `);
      console.log("\nDatos en la tabla Movie_Cast:");
      console.table(movieCastResult.rows);
  
      // Verificar los registros en la tabla Users
      const usersResult = await client.query(`
        SELECT * FROM Users;
      `);
      console.log("\nDatos en la tabla Users:");
      console.table(usersResult.rows);
  
      // Verificar los registros en la tabla User_Profiles
      const userProfilesResult = await client.query(`
        SELECT * FROM User_Profiles;
      `);
      console.log("\nDatos en la tabla User_Profiles:");
      console.table(userProfilesResult.rows);
  
      // Verificar los registros en la tabla Recommendations
      const recommendationsResult = await client.query(`
        SELECT * FROM Recommendations;
      `);
      console.log("\nDatos en la tabla Recommendations:");
      console.table(recommendationsResult.rows);
  
      // Verificar los registros en la tabla Watch_Providers
      const watchProvidersResult = await client.query(`
        SELECT * FROM Watch_Providers;
      `);
      console.log("\nDatos en la tabla Watch_Providers:");
      console.table(watchProvidersResult.rows);
  
    } catch (err) {
      console.error("Error al verificar las tablas o los datos:", err);
    } finally {
      await client.end();
    }
  };

verifyTablesAndData();
