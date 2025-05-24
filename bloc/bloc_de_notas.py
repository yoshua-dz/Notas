import streamlit as st
import requests # para solicitar el contenido de la url
from PIL import Image  #para manejo de imagenes
from io import BytesIO 

# Clase base
class Nota:
    def __init__(self, titulo, contenido):
        self.titulo = titulo
        self.contenido = contenido

    def mostrar(self):
        return f"Título: {self.titulo}\nContenido: {self.contenido}"

    def modificar_contenido(self, nuevo_contenido):
        self.contenido = nuevo_contenido

# Clase derivada: NotaTexto
class NotaTexto(Nota):
    def mostrar(self):
        return f"📝 Título: {self.titulo}\n{self.contenido}"

# Clase derivada: NotaLista
class NotaLista(Nota):
    def mostrar(self):
        lista = "\n".join(f"- {item.strip()}" for item in self.contenido.split(",")) #.join() pone todo lo de la lista hecha por el split()  en un mismo str y lo separa con \n 
        return f"📋 Título: {self.titulo}\n{lista}"

# Clase derivada: NotaImagen
class NotaImagen(Nota):
    def mostrar(self):
        return f"🖼️ Imagen: {self.titulo}\nURL: {self.contenido}"

# Clase para manejar varias notas
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

    def buscar_nota(self, titulo):
        return [n for n in self.notas if titulo.lower() in n.titulo.lower()] # Hace una lista que cumple con coincidir los caracteres buscados con los de los titulos de las notas

    def eliminar_nota(self, titulo):
        self.notas = [n for n in self.notas if n.titulo != titulo] # Hace una lista con los titulos que no son iguales a lo que se busco eliminar

def mostrar_imagen_desde_url(url, titulo):
    try:
        response = requests.get(url) # Obtiene lo de la url
        response.raise_for_status()  # Verifica que la respuesta sea válida
        img = Image.open(BytesIO(response.content)) # se hace un archivo en bytes para manejar la imagen
        st.image(img, caption=titulo, use_column_width=True)
    except Exception as e:
        st.error(f"No se pudo cargar la imagen: {e}")

# INTERFAZ CON STREAMLIT
st.set_page_config(page_title="Bloc de Notas", layout="centered") 
st.title("🗒️ Bloc de Notas Interactivo")

if "bloc" not in st.session_state:
    st.session_state.bloc = BlocDeNotas()

# Crear nota
st.header("➕ Crear una nueva nota")
tipo = st.selectbox("Tipo de nota", ["Texto", "Lista", "Imagen"])
titulo = st.text_input("Título de la nota")
contenido = st.text_area("Contenido (en caso de imagen, coloca URL)")

if st.button("Crear nota"):
    if titulo and contenido:
        st.session_state.bloc.crear_nota(tipo, titulo, contenido)
        st.success("✅ Nota creada con éxito")
    else:
        st.warning("Por favor, completa todos los campos.")

# Mostrar notas
st.header("📚 Ver todas las notas")
if st.session_state.bloc.mostrar_notas():
    for nota in st.session_state.bloc.mostrar_notas():
        st.markdown("---")
        if isinstance(nota, NotaImagen):
            st.image(nota.contenido, caption=nota.titulo, use_column_width=True)   
            st.text(nota.mostrar())
        else: 
            st.subheader(nota.titulo)
            st.text(nota.mostrar())
else:
    st.info("No hay notas aún.")
    
# Buscar nota
st.header("🔍 Buscar nota")
buscar = st.text_input("Buscar por título")
if buscar:
    resultados = st.session_state.bloc.buscar_nota(buscar)
    if resultados:
        for r in resultados:
            st.markdown("----")
            st.subheader(r.titulo)
            st.text(r.mostrar())
            if isinstance(r, NotaImagen):
                st.image(r.contenido, caption=r.titulo, use_column_width=True)
    else:
        st.info("No se encontraron notas.")

# Eliminar nota
st.header("❌ Eliminar una nota")
titulo_eliminar = st.text_input("Título exacto a eliminar")
if st.button("Eliminar"):
    st.session_state.bloc.eliminar_nota(titulo_eliminar)
    st.success("Nota eliminada (si existía)")

