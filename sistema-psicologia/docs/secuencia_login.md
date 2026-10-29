# Diagrama de Secuencia - Inicio de Sesión

A continuacion se muestra el diagrama de secuencia que representa el flujo completo del proceso de autenticacion de usuarios (Tutor y Psicologa) dentro del sistema.

```mermaid
sequenceDiagram
    autonumber
    actor Usuario as Tutor / Psicologa
    participant Form as Formulario (Vista HTML)
    participant App as app.py (Controlador Flask)
    participant Modelo as Modelo (Psicologa / Tutor)
    participant DB as Base de Datos (MySQL)

    Usuario->>Form: Ingresa correo/usuario y contrasena
    Form->>App: Envia peticion HTTP POST con credenciales
    App->>Modelo: Llama metodo de busqueda
    Modelo->>DB: Ejecuta consulta SQL parametrizada (%s)
    DB-->>Modelo: Retorna registro del usuario (con hash)
    Modelo-->>App: Retorna datos de credenciales
    
    alt Usuario encontrado en la BD
        App->>Modelo: Ejecuta verificar_contrasena()
        
        alt Contrasena correcta
            App->>App: Establece la sesion activa (session)
            App-->>Form: Redirige al panel principal
            Form-->>Usuario: Muestra el dashboard
        else Contrasena incorrecta
            App-->>Form: Retorna mensaje de error
            Form-->>Usuario: Muestra alerta en pantalla
        end
    else Usuario no existe
        App-->>Form: Retorna usuario no encontrado
        Form-->>Usuario: Muestra alerta en pantalla
    end