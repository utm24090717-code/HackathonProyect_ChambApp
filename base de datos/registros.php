<?php
include("conexion.php");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre     = $conn->real_escape_string($_POST['nombre']);
    $apellidos  = $conn->real_escape_string($_POST['apellidos']);
    $correo     = $conn->real_escape_string($_POST['correo']);
    $numero     = $conn->real_escape_string($_POST['numero']);
    $contrasena = $conn->real_escape_string($_POST['contrasena']);

    if (!empty($nombre) && !empty($apellidos) && !empty($correo) && !empty($numero) && !empty($contrasena)) {
        
        $sql = "INSERT INTO usuarios (nombre, apellidos, correo, numero, contrasena) 
                VALUES ('$nombre', '$apellidos', '$correo', '$numero', '$contrasena')";

        if ($conn->query($sql) === TRUE) {
            echo "✅ Cuenta creada con éxito";
        } else {
            echo "❌ Error: " . $conn->error;
        }
    } else {
        echo "⚠️ Todos los campos son obligatorios";
    }
}

$conn->close();
?>
