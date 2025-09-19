<?php

include("conexion.php");


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre    = $conn->real_escape_string($_POST['nombre']);
    $apellidos = $conn->real_escape_string($_POST['apellidos']);
    $correo    = $conn->real_escape_string($_POST['correo']);
    $telefono  = $conn->real_escape_string($_POST['telefono']);
    $contraseña  = $conn->real_escape_string($_POST['contraseña']);

    if (!empty($nombre) && !empty($apellidos) && !empty($correo) && !empty($telefono)&& !empty($contraseña)) {
        
        $sql = "INSERT INTO usuarios (nombre, apellidos, correo, telefono, contraseña) 
                VALUES ('$nombre', '$apellidos', '$correo', '$telefono','$contraseña')";

        if ($conn->query($sql) === TRUE) {
            echo "✅ Cuenta creada con éxito";
        } else {
            echo "❌ Error: " . $conn->error;
        }
    } else {
        echo "⚠️ Todos los campos son obligatorios";
    }
}

// Cerrar conexión
$conn->close();
?>