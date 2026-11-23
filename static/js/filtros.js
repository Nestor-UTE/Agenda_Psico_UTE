
function iniciarFiltros(configuracion) {
    const tabla = document.getElementById(configuracion.tablaId);

    if (!tabla) {
        return;
    }


    const filas = Array.from(
        tabla.querySelectorAll("tr[data-filtro]")
    );


    const buscador = document.getElementById("buscador");
    const filtroGrado = document.getElementById("filtro-grado");
    const filtroGrupo = document.getElementById("filtro-grupo");
    const filtroCarrera = document.getElementById("filtro-carrera");
    const filtroEstado = document.getElementById("filtro-estado");
    const filtroFecha = document.getElementById("filtro-fecha");

    const limpiarFecha = document.getElementById("limpiar-fecha");
    const ordenFecha = document.getElementById("orden-fecha");


    const sinResultados = document.getElementById("sin-resultados");


    // Obtener las carreras existentes sin repetirlas
    if (filtroCarrera) {
        const carreras = [
            ...new Set(
                filas.map(function (fila) {
                    return (fila.dataset.carrera || "").trim();
                })
            )
        ]
            .filter(Boolean)
            .sort();

        carreras.forEach(function (carrera) {
            const opcion = document.createElement("option");

            opcion.value = carrera;
            opcion.textContent = carrera;

            filtroCarrera.appendChild(opcion);
        });
    }


    function aplicarFiltros() {
        const texto = buscador?.value.trim().toLowerCase() || "";
        const grado = filtroGrado?.value || "";
        const grupo = filtroGrupo?.value.trim().toLowerCase() || "";
        const carrera = filtroCarrera?.value || "";
        const estado = filtroEstado?.value || "";
        const fecha = filtroFecha?.value || "";

        let visibles = 0;

        filas.forEach(function (fila) {
            const coincideTexto =
                !texto || fila.textContent.toLowerCase().includes(texto);

            const coincideGrado =
                !grado || fila.dataset.grado === grado;

            const coincideGrupo =
                !grupo ||
                (fila.dataset.grupo || "").toLowerCase().includes(grupo);

            const coincideCarrera =
                !carrera || fila.dataset.carrera === carrera;

            const coincideEstado =
                !estado || fila.dataset.estado === estado;

            const coincideFecha =
                !fecha || fila.dataset.fecha === fecha;

            const mostrar =
                coincideTexto &&
                coincideGrado &&
                coincideGrupo &&
                coincideCarrera &&
                coincideEstado &&
                coincideFecha;

            fila.style.display = mostrar ? "" : "none";

            if (mostrar) {
                visibles++;
            }
        });

        if (sinResultados) {
            sinResultados.hidden =
                visibles > 0 || filas.length === 0;
        }
    }

    // Ordenar registros por fecha y hora de la cita
    function ordenarRegistros() {
        if (!ordenFecha) return;

        const direccion = ordenFecha.dataset.orden;

        filas.sort(function (a, b) {
            const fechaA = a.dataset.fechaHora || a.dataset.fecha || "";
            const fechaB = b.dataset.fechaHora || b.dataset.fecha || "";

            // Los registros sin fecha quedan al final
            if (!fechaA && !fechaB) return 0;
            if (!fechaA) return 1;
            if (!fechaB) return -1;

            // En Agenda, mostrar primero las citas futuras
            if (direccion === "proximas" || direccion === "lejanas") {
                const ahora = new Date();

                const pasadaA = new Date(fechaA) < ahora;
                const pasadaB = new Date(fechaB) < ahora;

                // Las citas pasadas siempre quedan al final
                if (pasadaA !== pasadaB) {
                    return pasadaA ? 1 : -1;
                }

                return direccion === "proximas"
                    ? fechaA.localeCompare(fechaB)
                    : fechaB.localeCompare(fechaA);
            }

            // Conservar el ordenamiento de las otras pantallas
            return direccion === "reciente"
                ? fechaB.localeCompare(fechaA)
                : fechaA.localeCompare(fechaB);
        });

        filas.forEach(function (fila) {
            tabla.appendChild(fila);
        });
    }

    // Activar filtros mientras el usuario escribe
    [buscador, filtroGrupo].forEach(function (campo) {
        if (campo) {
            campo.addEventListener("input", aplicarFiltros);
        }
    });

    // Activar filtros al seleccionar una opción
    [filtroGrado, filtroCarrera, filtroEstado, filtroFecha].forEach(
        function (campo) {
            if (campo) {
                campo.addEventListener("change", aplicarFiltros);
            }
        }
    );

    // Alternar el orden sin afectar las otras pantallas
    if (ordenFecha) {
        ordenFecha.addEventListener("click", function () {
            const ordenActual = ordenFecha.dataset.orden;

            // Identificar si estamos en Agenda / Cita
            const esAgenda =
                ordenActual === "proximas" ||
                ordenActual === "lejanas";

            let nuevoOrden;
            let texto;

            if (esAgenda) {
                nuevoOrden = ordenActual === "proximas"
                    ? "lejanas"
                    : "proximas";

                texto = nuevoOrden === "proximas"
                    ? "Próximas primero"
                    : "Más lejanas primero";
            } else {
                // Mantener el comportamiento de otras pantallas
                nuevoOrden = ordenActual === "reciente"
                    ? "antiguo"
                    : "reciente";

                texto = nuevoOrden === "reciente"
                    ? "Más recientes"
                    : "Más antiguos";
            }

            ordenFecha.dataset.orden = nuevoOrden;

            const textoOrden =
                ordenFecha.querySelector("#texto-orden");

            if (textoOrden) {
                textoOrden.textContent = texto;
            }

            ordenFecha.setAttribute(
                "aria-label",
                esAgenda
                    ? "Ordenar citas: " + texto.toLowerCase()
                    : "Ordenar por fecha: " + texto.toLowerCase()
            );

            ordenarRegistros();
        });
    }

    // Mostrar la X cuando se seleccione una fecha
    if (filtroFecha && limpiarFecha) {
        limpiarFecha.hidden = !filtroFecha.value;

        filtroFecha.addEventListener("change", function () {
            limpiarFecha.hidden = !filtroFecha.value;
        });

        // Limpiar únicamente la fecha seleccionada
        limpiarFecha.addEventListener("click", function () {
            filtroFecha.value = "";
            limpiarFecha.hidden = true;
            aplicarFiltros();
        });
    }


    // Aplicar el orden y los filtros al cargar la página
    ordenarRegistros();
    aplicarFiltros();


}
