<?php
include("conexion.php");

// Función para guardar logs
function guardarLog($texto) {
    // Carpeta de logs dentro del proyecto
    $carpetaLogs = __DIR__ . '/logs';

    // Crear la carpeta si no existe
    if (!file_exists($carpetaLogs)) {
        mkdir($carpetaLogs, 0777, true);
    }

    // Archivo de log
    $archivoLog = $carpetaLogs . '/logs.txt';

    // Formatear el mensaje con fecha y hora
    $mensaje = "[" . date('Y-m-d H:i:s') . "] " . $texto . "\n";

    try {
        // Abrir archivo en modo append
        $archivo = fopen($archivoLog, 'a');
        if (!$archivo) {
            throw new Exception("No se pudo abrir el archivo de log.");
        }
        fwrite($archivo, $mensaje);
        fclose($archivo);
    } catch (Exception $e) {
        echo "Error al guardar log: " . $e->getMessage();
    }
}

// Iniciar log
guardarLog("PASO0 - Inicio del script");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    guardarLog("Método POST detectado");

    // Escapar datos recibidos del formulario
    $nombre     = $conn->real_escape_string($_POST['nombre']);
    $apellidos  = $conn->real_escape_string($_POST['apellidos']);
    $correo     = $conn->real_escape_string($_POST['correo']);
    $numero     = $conn->real_escape_string($_POST['numero']);
    $contrasena = $conn->real_escape_string($_POST['contrasena']);

    if (!empty($nombre) && !empty($apellidos) && !empty($correo) && !empty($numero) && !empty($contrasena)) {
        guardarLog("PASO1 - Todos los campos completos");

        $sql = "INSERT INTO usuarios (nombre, apellidos, correo, numero, contrasena) 
                VALUES ('$nombre', '$apellidos', '$correo', '$numero', '$contrasena')";

        guardarLog("PASO2 - SQL a ejecutar: " . $sql);

        try {
            if ($conn->query($sql) === TRUE) {
                guardarLog("PASO3 - Cuenta creada con éxito");
                echo "Cuenta creada con éxito";
            } else {
                guardarLog("PASO4 - Error al insertar: " . $conn->error);
                echo "Error: " . $conn->error;
            }
        } catch (Exception $e) {
            guardarLog("Error capturado en try-catch: " . $e->getMessage());
            echo "Error: " . $e->getMessage();
        }
    } else {
        guardarLog("Error - Faltan campos obligatorios");
        echo "Todos los campos son obligatorios";
    }
} else {
    guardarLog("Error - No se recibió método POST");
    echo "Acceso inválido al script";
}

// Cerrar conexión
$conn->close();
?>
