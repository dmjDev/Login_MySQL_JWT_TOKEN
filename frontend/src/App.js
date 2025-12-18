import { useEffect, useState } from "react";
import UsersBox from "./components/UsersBox";
import CreateUser from "./components/CreateUser";

// FINCIÓN QUE SE EJECUTA AL INICIAR EL FRONTEND
function App() {
  // useEffect nos permite ejecutar una ruta API y devuelve el contenido de esta ruta al ser invocada con .then
  // introducimos el resultado en una constante users a través de la función setUsers
  // en esta primera declaración de la constante users se le da un estado de array vacío para inicializarla: useState([])
  const [users, setUsers] = useState([])
  useEffect(() => {
    // fetch('http://localhost:8000/api/users')   // CONEXIÓN BACKEND LOCAL DE NUESTRO SERVIDOR CON EL CONTENEDOR DOCKER CUANDO ESTE APUNTA AL PUERTO 8000
    fetch('http://172.18.0.3:8000/api/users')     // CONEXIÓN BACKEND MEDIANTE LOS DNS DE LA RED DOCKER CON EL CONTENEDOR DOCKER SIN PUERTOS ABIERTOS
    .then(res => res.json())
    .then(res => setUsers(res))
  }, [])
  return (
    // EN ESTA SECCIÓN PONDREMOS TODO LO QUE QUERAMOS QUE APAREZCA EN NUESTRO FRONTEND DENTRO DE UN <MAIN>
    // (POST/api/users) CREATEUSER (etiqueta HTML personalizada) Mostramos el formulario para el registro de nuevos usuarios 
    // (GET/api/users) USERSBOX (etiqueta HTML personalizada) Mapeamos los datos obtenidos en la consulta, para todos los usuarios de la base de datos
    <main>
      <h2>FrontEnd&BackEnd APP</h2>
      <CreateUser />
      {
        users.map(user => (
          <UsersBox 
          username={user.username} 
          nombre_completo={user.nombre_completo} 
          fecha_nacimiento={user.fecha_nacimiento} 
          email={user.email} 
          key={user.username} />
        ))
      }
    </main>
  );
}

// CON ESTA SENTENCIA PODEMOS VER EL CONTENIDO DE LA FUNCIÓN APP EN index.js, 
// EL CUAL ESTÁ DEFINIENDO EL CONTENIDO DE LA ETIQUETA HTML CON ID=root DE INDEX.HTML
export default App;
