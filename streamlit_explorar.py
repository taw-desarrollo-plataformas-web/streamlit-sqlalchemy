# streamlit_explorar.py

import streamlit as st
from db import get_session

# Importa las clases que definiste en clases.py
from clases import Departamento, Instructor, Curso, Estudiante, Inscripcion, Tarea, Entrega


st.set_page_config(page_title="Explorador de objetos SQLAlchemy", layout="wide")


def listar_departamentos():
    """
    Muestra todos los departamentos y, en un expander, sus cursos con título y profesor.
    """
    st.header("Departamentos")
    session = get_session()
    departamentos = session.query(Departamento).all()


    if not departamentos:
        st.info("No hay registros en 'departamento'.")
        session.close()
        return

    # Para cada Departamento, mostramos un expander que contiene su lista de cursos
    for dept in departamentos:
        with st.expander(f"ID {dept.id} → {dept.nombre}", expanded=False):
            # Mostrar atributos básicos
            st.write(f"**ID:** {dept.id}")
            st.write(f"**Nombre:** {dept.nombre}")

            # Si el departamento tiene cursos relacionados, listarlos
            if dept.cursos:
                st.write("**Cursos asociados:**")
                # Usamos st.table para mostrar una tabla sencilla con el id, título e instructor
                filas = []
                for c in dept.cursos:
                    filas.append({
                        "Curso ID": c.id,
                        "Título": c.titulo,
                        "Instructor": c.instructor.nombre,
                        "Nro. Inscripciones": len(c.inscripciones),
                        "Tareas pendientes": len(c.tareas),
                    })
                st.table(filas)
            else:
                st.write("_No hay cursos asociados a este departamento._")
    session.close()

def listar_instructores():
    """
    Muestra todos los instructores y, dentro de cada expander, sus cursos.
    """
    st.header("Instructores")
    session = get_session()
    instructores = session.query(Instructor).all()


    if not instructores:
        st.info("No hay registros en 'instructor'.")
        session.close()
        return

    for ins in instructores:
        with st.expander(f"ID {ins.id} → {ins.nombre}", expanded=False):
            st.write(f"**ID:** {ins.id}")
            st.write(f"**Nombre:** {ins.nombre}")

            if ins.cursos:
                st.write("**Cursos que dicta:**")
                filas = []
                for c in ins.cursos:
                    filas.append({
                        "Curso ID": c.id,
                        "Título": c.titulo,
                        "Departamento": c.departamento.nombre,
                        "Nro. Inscripciones": len(c.inscripciones),
                    })
                st.table(filas)
            else:
                st.write("_Este instructor no dicta ningún curso._")
    session.close()

def listar_cursos():
    """
    Muestra todos los cursos y, para cada uno, desplega detalles de departamento, instructor,
    número de inscripciones, tareas y, opcional, lista de estudiantes inscritos.
    """
    st.header("Cursos")
    session = get_session()
    cursos = session.query(Curso).all()

    if not cursos:
        st.info("No hay registros en 'curso'.")
        session.close()
        return

    for c in cursos:
        with st.expander(f"ID {c.id} → {c.titulo}", expanded=False):
            # Atributos propios
            st.write(f"**ID:** {c.id}")
            st.write(f"**Título:** {c.titulo}")
            dept_nombre = c.departamento.nombre
            instr_nombre = c.instructor.nombre
            st.write(f"**Departamento:** {dept_nombre}")
            st.write(f"**Instructor:** {instr_nombre}")
            st.write(f"**Nro. Inscripciones:** {len(c.inscripciones)}")
            st.write(f"**Nro. Tareas:** {len(c.tareas)}")

            # Mostrar lista de estudiantes inscritos con fecha de inscripción
            if c.inscripciones:
                st.write("**Detalles de inscripciones:**")
                filas_ins = []
                for insc in c.inscripciones:
                    filas_ins.append({
                        "Estudiante ID": insc.estudiante.id,
                        "Estudiante": insc.estudiante.nombre,
                        "Fecha inscripción": insc.fecha_inscripcion.strftime("%Y-%m-%d %H:%M"),
                    })
                st.table(filas_ins)
            else:
                st.write("_No hay inscripciones en este curso._")

            # Mostrar lista de tareas y cuántas entregas tiene cada tarea
            if c.tareas:
                st.write("**Tareas del curso:**")
                filas_t = []
                for t in c.tareas:
                    filas_t.append({
                        "Tarea ID": t.id,
                        "Título tarea": t.titulo,
                        "Fecha entrega": t.fecha_entrega.strftime("%Y-%m-%d"),
                        "Entregas recibidas": len(t.entregas),
                    })
                st.table(filas_t)
            else:
                st.write("_No hay tareas en este curso._")
    session.close()

def listar_estudiantes():
    """
    Muestra todos los estudiantes y, dentro de cada expander, las inscripciones y entregas.
    """
    st.header("Estudiantes")
    session = get_session()
    estudiantes = session.query(Estudiante).all()

    if not estudiantes:
        st.info("No hay registros en 'estudiante'.")
        session.close()


    for e in estudiantes:
        with st.expander(f"ID {e.id} → {e.nombre}", expanded=False):
            st.write(f"**ID:** {e.id}")
            st.write(f"**Nombre:** {e.nombre}")

            # Inscripciones
            if e.inscripciones:
                st.write("**Cursos en los que está inscrito:**")
                filas_ins = []
                for insc in e.inscripciones:
                    filas_ins.append({
                        "Curso ID": insc.curso.id,
                        "Título curso": insc.curso.titulo,
                        "Fecha inscripción": insc.fecha_inscripcion.strftime("%Y-%m-%d %H:%M"),
                    })
                st.table(filas_ins)
            else:
                st.write("_El estudiante no está inscrito en ningún curso._")

            # Entregas
            if e.entregas:
                st.write("**Entregas realizadas:**")
                filas_ent = []
                for ent in e.entregas:
                    filas_ent.append({
                        "Entrega ID": ent.id,
                        "Tarea": ent.tarea.titulo,
                        "Curso": ent.tarea.curso.titulo,
                        "Fecha envío": ent.fecha_envio.strftime("%Y-%m-%d %H:%M"),
                        "Calificación": float(ent.calificacion),
                    })
                st.table(filas_ent)
            else:
                st.write("_Este estudiante no ha hecho ninguna entrega._")
    session.close()

def listar_inscripciones():
    """
    Muestra todas las inscripciones y, para cada una, detalla estudiante y curso.
    """
    st.header("Inscripciones")
    session = get_session()
    inscripciones = session.query(Inscripcion).all()

    if not inscripciones:
        st.info("No hay registros en 'inscripcion'.")
        session.close()
        return

    filas = []
    for insc in inscripciones:
        filas.append({
            "Estudiante ID": insc.estudiante.id,
            "Estudiante": insc.estudiante.nombre,
            "Curso ID": insc.curso.id,
            "Título curso": insc.curso.titulo,
            "Fecha inscripción": insc.fecha_inscripcion.strftime("%Y-%m-%d %H:%M"),
        })
    st.table(filas)
    session.close()


def listar_tareas():
    """
    Muestra todas las tareas con detalle de curso e instructor.
    """
    st.header("Tareas")
    session = get_session()
    tareas = session.query(Tarea).all()

    if not tareas:
        st.info("No hay registros en 'tarea'.")
        session.close()
        return

    filas = []
    for t in tareas:
        filas.append({
            "Tarea ID": t.id,
            "Título tarea": t.titulo,
            "Curso ID": t.curso.id,
            "Título curso": t.curso.titulo,
            "Fecha entrega": t.fecha_entrega.strftime("%Y-%m-%d"),
            "Entregas recibidas": len(t.entregas),
        })
    st.table(filas)
    session.close()


def listar_entregas():
    """
    Muestra todas las entregas resolviendo relaciones:
    estudiante, tarea y curso asociado.
    """
    st.header("Entregas")
    session = get_session()
    entregas = session.query(Entrega).all()


    if not entregas:
        st.info("No hay registros en 'entrega'.")
        session.close()
        return

    filas = []
    for ent in entregas:
        filas.append({
            "Entrega ID": ent.id,
            "Estudiante": ent.estudiante.nombre,
            "Curso": ent.tarea.curso.titulo,
            "Tarea": ent.tarea.titulo,
            "Fecha envío": ent.fecha_envio.strftime("%Y-%m-%d %H:%M"),
            "Calificación": float(ent.calificacion),
        })
    st.table(filas)
    session.close()


def main():
    st.title("Explorador de objetos SQLAlchemy en Streamlit")

    entidad = st.sidebar.selectbox(
        "Elija la entidad que desea explorar:",
        (
            "Departamento",
            "Instructor",
            "Curso",
            "Estudiante",
            "Inscripción",
            "Tarea",
            "Entrega",
        ),
    )

    if entidad == "Departamento":
        listar_departamentos()
    elif entidad == "Instructor":
        listar_instructores()
    elif entidad == "Curso":
        listar_cursos()
    elif entidad == "Estudiante":
        listar_estudiantes()
    elif entidad == "Inscripción":
        listar_inscripciones()
    elif entidad == "Tarea":
        listar_tareas()
    elif entidad == "Entrega":
        listar_entregas()


if __name__ == "__main__":
    main()
