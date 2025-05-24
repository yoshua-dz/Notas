import streamlit as st
from PIL import Image

class Nota:
    def __init__(self, titulo, contenido):
        self.titulo = titulo
        self.contenido = contenido

    def mostrar(self):
        pass

class NotaTexto(Nota):
    def mostrar (self):
        return f"Titulo: {self.titulo}\n Contenido: {self.contenido}"

class NotaLista(Nota):
    def mostrar(self):
        lista = "\n".join(f" - {item.strip()}" for item in self.contenido.split(","))
        return f"Titulo: {self.titulo}\n contenido:\n {lista}"

class NotaImagen(Nota):
    def mostrar(self):
        return f"Titulo: {self.titulo}\n(Imagen)"
        
class BlocDeNotas:
    def __init__(self):
        self.notas = []

    def crear_nota(self, tipo, titulo, contenido):
        if tipo == "Texto":
            nota = NotaTexto(titulo, contenido)
        elif tipo == "Lista":
            nota = NotaLista(titulo, contenido)
        elif tipo == "Imagen":
            nota = NotaImagen(titulo, contenido)
        else:
            return 
        self.notas.append(nota)

    def mostrar_notas(self):
        return self.notas
    
    def buscar_notas(self, titulo):
        return [n for n in self.notas if titulo.lower() in n.titulo.lower()]
    
    def eliminar_nota(self, titulo):
        self.notas = [n for n in self.notas if titulo.lower() != n.titulo.lower()]

if 'bloc' not in st.session_state:
    st.session_state.bloc = BlocDeNotas()

st.set_page_config(page_title="Bloc de notas")
st.title ("Bloc de Notas")

st.header("Crear una nueva nota")
tipo = st.selectbox("Tipo de nota", ["Texto", "Lista", "Imagen"])
titulo = st.text_input("Titulo de la nota")
contenido = st.text_input ("Contenido")

if st.button ("Crear nota"):
    if titulo and contenido:
        st.session_state.bloc.crear_nota(tipo, titulo, contenido)
        st.success("Nota creada exitosamente")
    else:
        st.warning("Por favor, completar todos los campos")

st.header("Mostrar todas las notas")
if st.session_state.bloc.mostrar_notas():
    for nota in st.session_state.bloc.mostrar_notas():
        st.markdown("---")
        if isinstance(nota, NotaImagen):
            st.write("Contenido de la nota:", nota.contenido)
            st.image(nota.contenido, caption=nota.titulo, use_column_width=True)   
            st.text(nota.mostrar())
        else: 
            st.subheader(nota.titulo)
            st.text(nota.mostrar())
else:
    st.info("No hay notas aún.")

st.header("Buscar notas")
busqueda = st.text_input("Buscar por titulo")
if busqueda:
    resultados = st.session_state.bloc.buscar_notas(busqueda)
    if resultados:
        for r in resultados:
            st.markdown("----")
            st.subheader(r.titulo)
            st.text(r.mostrar())
            if isinstance(r, NotaImagen):
                try:
                    st.image(r.contenido, caption=r.titulo, use_column_width=True)
                except:
                    st.error("No se pudo cargar la imagen.")
    else:
        st.info("No se encontraron notas")

st.header("Eliminar notas")
titulo_eliminar = st.text_input("titulo de la nota a eliminar")
if st.button("Eliminar"):
    st.session_state.bloc.eliminar_nota(titulo_eliminar)
    st.success("Se ha eliminado la nota ")


