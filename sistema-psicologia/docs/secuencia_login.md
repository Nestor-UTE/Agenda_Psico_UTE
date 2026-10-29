# Diagrama de Secuencia - Inicio de Sesion# Diagrama de Secuencia - Inicio de Sesion

A continuacion se muestra el diagrama de secuencia que representa el flujo completo del proceso de autenticacion de usuarios (Tutor y Psicologa) dentro del sistema, abarcando desde la interfaz web hasta la validacion en la base de datos.

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
    App->>Modelo: Llama metodo de busqueda (ej. buscar_por_usuario / buscar_por_correo)
    Modelo->>DB: Ejecuta consulta SQL parametrizada (%s)
    DB-->>Modelo: Retorna registro del usuario (incluyendo contrasena en hash)
    Modelo-->>App: Retorna objeto con datos de credenciales
    
    alt Usuario encontrado en la BD
        App->>Modelo: Ejecuta verificar_contrasena(contrasena_plana)
        Note over App,Modelo: Se valida el hash mediante werkzeug.security (check_password_hash)
        
        alt Contrasena correcta
            App->>App: Establece la sesion activa (session)
            App-->>Form: Redirige al panel principal (Redirect)
            Form-->>Usuario: Muestra el dashboard correspondiente
        else Contrasena incorrecta
            App-->>Form: Retorna mensaje de error de credenciales
            Form-->>Usuario: Muestra alerta visual de error en pantalla
        end
    else Usuario no existe
        App-->>Form: Retorna mensaje de usuario no encontrado
        Form-->>Usuario: Muestra alerta visual de error en pantalla
    endn

A continuacion se muestra el diagrama de secuencia que representa el flujo completo del proceso de autenticacion de usuarios (Tutor y Psicologa) dentro del sistema, abarcando desde la interfaz web hasta la validacion en la base de datos.

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
    App->>Modelo: Llama metodo de busqueda (ej. buscar_por_usuario / buscar_por_correo)
    Modelo->>DB: Ejecuta consulta SQL parametrizada (%s)
    DB-->>Modelo: Retorna registro del usuario (incluyendo contrasena en hash)
    Modelo-->>App: Retorna objeto con datos de credenciales
    
    alt Usuario encontrado en la BD
        App->>Modelo: Ejecuta verificar_contrasena(contrasena_plana)
        Note over App,Modelo: Se valida el hash mediante werkzeug.security (check_password_hash)
        
        alt Contrasena correcta
            App->>App: Establece la sesion activa (session)
            App-->>Form: Redirige al panel principal (Redirect)
            Form-->>Usuario: Muestra el dashboard correspondiente
        else Contrasena incorrecta
            App-->>Form: Retorna mensaje de error de credenciales
            Form-->>Usuario: Muestra alerta visual de error en pantalla
        end
    else Usuario no existe
        App-->>Form: Retorna mensaje de usuario no encontrado
        Form-->>Usuario: Muestra alerta visual de error en pantalla
    end