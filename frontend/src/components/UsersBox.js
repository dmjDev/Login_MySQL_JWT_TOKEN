// Creamos una etiqueta HTML propia mediante REACT para mostrar el contenido del resultado de la API (GET/api/users) llamada en App.js
// Estructurando el HTML para mostrar los datos destro de la función App de App.js

export default function UsersBox({username, nombre_completo, fecha_nacimiento, email}){
    return (
        <article>
            <h3>{nombre_completo}</h3>
            <p>{username}</p>
            <p>{fecha_nacimiento}</p>
            <p>{email}</p>
        </article>
    )
}