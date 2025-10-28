import streamlit as st
import json
import os
import shutil 

# ----------------------------------------------------
# DEFINICIÓN DE ARCHIVOS
# ----------------------------------------------------
CONFIG_FILE = 'config_cols.json'
PERSISTENCE_FILE = 'datos_maestro.csv' 
IMAGE_FOLDER = 'imagenes_persistentes' 

# Función para cargar la configuración de columnas (con UTF-8)
def load_config():
    """Carga la configuración actual desde el archivo JSON, usando UTF-8."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f: 
                return json.load(f)
        except Exception as e:
            st.error(f"Error al leer config_cols.json: {e}. Se cargará la configuración de emergencia.")
            return {
                "CONDICIONES_INSPECCION": ["DAÑO EN EMPAQUE", "DAÑO FISICO", "ACCESORIOS COMPLETOS"],
                "COLUMNAS_IMAGEN": ["FOTO DE SERIE", "FOTO DEL EMPAQUE"]
            }
    return {
        "CONDICIONES_INSPECCION": ["DAÑO EN EMPAQUE", "DAÑO FISICO", "ACCESORIOS COMPLETOS", "PARILLA EN MAL ESTADO", "PRESENTA RESTOS METALICOS (VIRUTAS)", "TAPAS PRESENTAN OXIDO", "PRESENTA RAYAS", "TARJETA DE GARANTÍA", "TIENE ETIQUETA DE EFICIENCIA ENERGETICA"],
        "COLUMNAS_IMAGEN": ["FOTO DE SERIE", "FOTO DEL EMPAQUE", "FOTO DE PRODUCTO COMPLETO", "FOTO PARTE TRASERA", "FOTO DE OBSERVACIONES A 50 CM (VIRUTAS)", "FOTO DE OBSERVACIONES CERCA (VIRUTAS)", "FOTO DE OBSERVACIONES A 50 CM (OXIDO EN TAPILLAS)", "FOTO DE OBSERVACIONES CERCA (OXIDO EN TAPILLAS)", "FOTO DE OBSERVACIONES A 50 CM (MANCHAS)", "FOTO DE OBSERVACIONES CERCA (MANCHAS)", "FOTO DE OBSERVACIONES A 50 CM (RAYAS)", "FOTO DE OBSERVACIONES CERCA (RAYAS)", "FOTO DE ACCESORIOS"]
    }

def save_config(new_config):
    """Guarda la nueva configuración en el archivo JSON (con UTF-8)."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f: # Uso de UTF-8 para guardar
            json.dump(new_config, f, indent=4, ensure_ascii=False) # ensure_ascii=False para guardar acentos
        st.success("✅ Configuración de columnas guardada. Los cambios serán visibles al usar la aplicación.")
    except Exception as e:
        st.error(f"❌ Error al guardar la configuración: {e}")

# ----------------------------------------------------
# PÁGINA DE ADMINISTRACIÓN DE COLUMNAS
# ----------------------------------------------------

def admin_page_main():
    st.title("⚙️ Administración de Columnas Dinámicas")
    st.markdown("Aquí puede añadir o eliminar las opciones de chequeo y las columnas de fotos. Cada opción debe estar en una **línea separada**.")

    current_config = load_config()

    # --- Bloque de Condiciones de Inspección ---
    st.header("1. Condiciones de Inspección (Checkboxes)")
    current_condiciones = "\n".join(current_config["CONDICIONES_INSPECCION"])

    new_condiciones_input = st.text_area(
        "Escriba una condición por línea (Ej: TORNILLO FALTANTE)",
        value=current_condiciones,
        height=200,
        key="condiciones_input"
    )

    # --- Bloque de Columnas de Fotos ---
    st.header("2. Columnas de Fotos (Encabezados)")
    current_imagenes = "\n".join(current_config["COLUMNAS_IMAGEN"])

    new_imagenes_input = st.text_area(
        "Escriba una columna de foto por línea (Ej: FOTO DE EMPAQUE ROTO)",
        value=current_imagenes,
        height=200,
        key="imagenes_input"
    )

    st.markdown("---")

    if st.button("💾 Guardar y Aplicar Cambios de Columnas", type="primary"):
        
        # Procesar los inputs de texto (eliminar líneas vacías y espacios)
        new_condiciones_list = [c.strip() for c in new_condiciones_input.split('\n') if c.strip()]
        new_imagenes_list = [i.strip() for i in new_imagenes_input.split('\n') if i.strip()]
        
        # Crear la nueva configuración
        new_config = {
            "CONDICIONES_INSPECCION": new_condiciones_list,
            "COLUMNAS_IMAGEN": new_imagenes_list
        }
        
        # Guardar y notificar al usuario
        save_config(new_config)
        st.warning("⚠️ Nota: Para que los cambios sean visibles en el formulario de Home, debe recargar la aplicación.")

    st.markdown("---")
    st.header("3. Herramientas de Datos")

    # Opción para limpiar todos los datos
    if st.button("🔥 ELIMINAR TODOS LOS REGISTROS Y ARCHIVOS PERSISTENTES", type="secondary"):
        
        if st.checkbox("Confirmo que deseo ELIMINAR PERMANENTEMENTE todos los registros (CSV) y todas las fotos (Carpeta de imágenes). ESTO ES IRREVERSIBLE.", key='confirm_delete'):
            
            if os.path.exists(PERSISTENCE_FILE):
                 os.remove(PERSISTENCE_FILE)
            if os.path.exists(IMAGE_FOLDER):
                 shutil.rmtree(IMAGE_FOLDER) 
            
            st.success("✅ Registros persistentes y archivos de imágenes eliminados con éxito. Vuelva a la página principal y reinicie la aplicación.")
        else:
            st.info("Debe confirmar la eliminación.")

admin_page_main()