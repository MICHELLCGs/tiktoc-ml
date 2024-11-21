const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  user: 'usertiktoc',
  password: 'tiktocpass',
  database: 'tiktocdb',
});

async function clearCustomTypes() {
  try {
    await client.connect();
    console.log('Conexión exitosa a la base de datos.');

    // Buscar y eliminar todos los tipos definidos por el usuario
    const dropTypesQuery = `
      DO $$ 
      DECLARE
        t RECORD;
      BEGIN
        FOR t IN (SELECT typname FROM pg_type WHERE typcategory = 'U' AND typnamespace = 'public'::regnamespace) LOOP
          EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(t.typname) || ' CASCADE';
        END LOOP;
      END $$;
    `;

    await client.query(dropTypesQuery);

    console.log('Todos los tipos personalizados han sido eliminados.');
  } catch (error) {
    console.error('Error al borrar los tipos:', error);
  } finally {
    await client.end();
    console.log('Conexión cerrada.');
  }
}

clearCustomTypes();
