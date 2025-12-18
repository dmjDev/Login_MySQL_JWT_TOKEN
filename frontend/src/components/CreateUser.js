import { useState } from "react";

// Función CreateUser
// Genera las contantes que almacenarán los datos del formulario y las inicializa
// Define las funciones que manejarán los eventos onClick de cada elemento del formulario
// Devuelve el formulario con todos los datos necesario que pide 
export default function CreateUser(){
    const [ text_username, setText_username ] = useState('')
    const [ text_nombre_completo, setText_nombre_completo ] = useState('')
    const [ text_fecha_nacimiento, setText_fecha_nacimiento ] = useState('')
    const [ text_email, setText_email ] = useState('')
    const [ check_disabled, setCheck_disabled ] = useState(true)
    const [ text_fecha_registro, setText_fecha_registro ] = useState('')
    const [ text_rol, setText_rol ] = useState("0")
    const [ text_ultimo_login, setText_ultimo_login ] = useState('')
    const [ text_hashed_password, setText_hashed_password ] = useState('')

    function handleText_username(e){
        setText_username(e.target.value)
    }
    function handleText_nombre_completo(e){
        setText_nombre_completo(e.target.value)
    }
    function handleText_fecha_nacimiento(e){
        setText_fecha_nacimiento(e.target.value)
    }
    function handleText_email(e){
        setText_email(e.target.value)
    }
    function handleCheck_disabled(e){
        setCheck_disabled(e.target.checked)
    }
    function handleText_fecha_registro(e){
        setText_fecha_registro(e.target.value)
    }
    function handleText_rol(e){
        setText_rol(e.target.value)
    }
    function handleText_ultimo_login(e){
        setText_ultimo_login(e.target.value)
    }
    function handleText_hashed_password(e){
        setText_hashed_password(e.target.value)
    }    

    // function handleClickForm(e){
    const handleClickForm = (e) => {
        e.preventDefault()          // Evitamos la pulsación por defecto del botón de envío de formulario
        showData()                  // Mostramos los datos enviados al BackEnd en consola
        
        // Conectamos con la API del BackEnd para enviar los datos (POST/api/users)
        // fetch('http://localhost:8000/api/users')     // CONEXIÓN BACKEND LOCAL DE NUESTRO SERVIDOR CON EL CONTENEDOR DOCKER CUANDO ESTE APUNTA AL PUERTO 8000
        fetch('http://172.18.0.3:8000/api/users/', {    // CONEXIÓN BACKEND MEDIANTE LOS DNS DE LA RED DOCKER CON EL CONTENEDOR DOCKER SIN PUERTOS ABIERTOS
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({
                username: text_username,
                nombre_completo: text_nombre_completo,
                fecha_nacimiento: text_fecha_nacimiento,
                email: text_email,
                disabled: check_disabled,
                fecha_registro: text_fecha_registro,
                rol: text_rol,
                ultimo_login: text_ultimo_login,
                hashed_password: text_hashed_password            
            })
        }).then(() => {
            setText_username('')
            setText_nombre_completo('')
            setText_fecha_nacimiento('')
            setText_email('')
            setCheck_disabled(true)
            setText_fecha_registro('')
            setText_rol("0")
            setText_ultimo_login('')
            setText_hashed_password('')
        })
    }
    return(
        <form onSubmit={handleClickForm}>
            <label htmlFor="username">Nombre de usuario</label>
            <input id="username" type="text" onChange={handleText_username} value={text_username} /><br />
            <label htmlFor="nombre_completo">Nombre y apellidos</label>
            <input id="nombre_completo" type="text" onChange={handleText_nombre_completo} value={text_nombre_completo} /><br />
            <label htmlFor="fecha_nacimiento">Fecha de nacimiento</label>
            <input id="fecha_nacimiento" type="date" onChange={handleText_fecha_nacimiento} value={text_fecha_nacimiento} /><br />
            <label htmlFor="email">Email</label>
            <input id="email" type="email" onChange={handleText_email} value={text_email} /><br />
            <label htmlFor="disabled">Desactivado</label>
            <input id="disabled" type="checkbox" onChange={handleCheck_disabled} checked={check_disabled} /><br />
            <label htmlFor="fecha_registro">Fecha de registro</label>
            <input id="fecha_registro" type="date" onChange={handleText_fecha_registro} value={text_fecha_registro} /><br />
            <label htmlFor="rol">Rol de usuario</label>
            <select name="rol" id="rol" onChange={handleText_rol} value={text_rol}>
                <option value="0">Usuario estándar</option>
                <option value="10">Administrador</option>
            </select><br />
            <label htmlFor="ultimo_login">Fecha último acceso</label>
            <input id="ultimo_login" type="date" onChange={handleText_ultimo_login} value={text_ultimo_login} /><br />
            <label htmlFor="hashed_password">Contraseña de usuario</label>
            <input id="hashed_password" type="password" onChange={handleText_hashed_password} value={text_hashed_password} /><br />
            <input type="submit" value="Registrarse" />
        </form>
    )

    function showData(){
        console.log(text_username)
        console.log(text_nombre_completo)
        console.log(text_fecha_nacimiento)
        console.log(text_email)
        console.log(check_disabled)
        console.log(text_fecha_registro)
        console.log(text_rol)
        console.log(text_ultimo_login)
        console.log(text_hashed_password)        
    }
}