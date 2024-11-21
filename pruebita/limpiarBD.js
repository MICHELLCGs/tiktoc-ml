const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  user: 'usertiktoc',
  password: 'tiktocpass',
  database: 'tiktocdb',
});

async function clearDatabase() {
  try {
    await client.connect();
    console.log('Conexión exitosa a la base de datos.');

    // Deshabilitar restricciones de llave foránea temporalmente
    await client.query('SET session_replication_role = replica;');

    // Eliminar todas las tablas
    const dropTablesQuery = `
      DO $$ DECLARE
        r RECORD;
      BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
          EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
      END $$;
    `;

    await client.query(dropTablesQuery);

    // Volver a habilitar restricciones de llave foránea
    await client.query('SET session_replication_role = DEFAULT;');

    console.log('Todas las tablas y datos han sido eliminados.');
  } catch (error) {
    console.error('Error al borrar la base de datos:', error);
  } finally {
    await client.end();
    console.log('Conexión cerrada.');
  }
}

clearDatabase();