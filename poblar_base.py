from sqlalchemy.orm import Session
from faker import Faker
from datetime import timedelta, datetime
from clases import engine, Departamento, Instructor, Curso, Estudiante, Inscripcion, Tarea, Entrega

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import cadena_base_datos
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Crear algunos departamentos fijos
departamentos = [Departamento(nombre=n) for n in ['CS', 'Historia', 'Arte', 'Física']]
session.add_all(departamentos)
session.flush()

# Generar instructores aleatorios
instructores = [Instructor(nombre=fake.name()) for _ in range(10)]
session.add_all(instructores)
session.flush()

# Crear cursos mixtos
mis_cursos = [
    "Fundamentos de Programación",
    "Álgebra Lineal",
    "Estructuras de Datos",
    "Métodos Numéricos",
    "Física Clásica",
    "Química Orgánica",
    "Biología Celular",
    "Estadística para Ciencias Sociales",
    "Microeconomía",
    "Macroeconomía",
    "Historia Contemporánea",
    "Filosofía de la Ciencia",
    "Sociología de la Educación",
    "Psicología del Desarrollo",
    "Lenguaje y Comunicación",
    "Diseño de Bases de Datos",
    "Redes de Computadores",
    "Inteligencia Artificial",
    "Gestión de Proyectos",
    "Ética Profesional"
]

cursos = []

for x in mis_cursos:
    dept = fake.random_element(departamentos)
    instr = fake.random_element(instructores)
    cursos.append(Curso(
        titulo=x,
        departamento=dept, instructor=instr
    ))
session.add_all(cursos)
session.flush()

# Generar estudiantes e inscripciones
estudiantes = [Estudiante(nombre=fake.name()) for _ in range(50)]
session.add_all(estudiantes)
session.flush()

for est in estudiantes:
    # cada estudiante inscrito en 1–3 cursos aleatorios
    for curso in fake.random_elements(cursos, length=fake.random_int(min=1, max=3), unique=True):
        ins = Inscripcion(
            estudiante=est,
            curso=curso,
            fecha_inscripcion=fake.date_time_between(start_date='-1y', end_date='now')
        )
        session.add(ins)

# Generar tareas y entregas
for curso in cursos:
    for _ in range(2):  # dos tareas por curso
        fecha_entrega = fake.future_date(end_date='+60d')
        tarea = Tarea(curso=curso, titulo=fake.sentence(nb_words=4), fecha_entrega=fecha_entrega)
        session.add(tarea)
        session.flush()
        # algunas entregas
        inscritos = [i.estudiante for i in curso.inscripciones]
        for est in fake.random_elements(inscritos, length=fake.random_int(0, len(inscritos)), unique=True):
            entrega = Entrega(
                tarea=tarea, estudiante=est,
                fecha_envio=fake.date_time_between(start_date='-30d', end_date=fecha_entrega),
                calificacion=round(fake.pyfloat(min_value=0, max_value=10), 2)
            )
            session.add(entrega)

session.commit()
session.close()
