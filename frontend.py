from pygame import Rect, font, display, init, MOUSEBUTTONDOWN, QUIT, event, draw, K_BACKSPACE, quit, KEYDOWN, K_RETURN
from declaraciones import crear_imagen, decodificar

# Inicialización de Pygame
init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255) 
GRAY = (200, 200, 200) 
ACTIVE_COLOR = (173, 216, 230)  # Azul claro

# Definir dimensiones de la ventana
size = (1200, 800)
screen = display.set_mode(size)
display.set_caption("CoDeCod2PnG v1.2") #Titulo de la ventana

# Fuente para el texto
font = font.SysFont('Arial', 25)

# Botones
button_codificar = Rect(200, 100, 200, 50)
button_decodificar = Rect(200, 200, 200, 50)
button_volver = Rect(200, 300, 200, 50)
button_ayuda = Rect(450, 50, 100, 50)  # Botón para "Ayuda"
button_volver_ayuda = Rect(50, 700, 200, 50)  # Botón "Volver" en la pantalla de ayuda

# Texto de ayuda dividido en partes para ser mostrado en líneas separadas
ayuda_textos = [
    "Bienvenido al programa de codificación y decodificación.",
    "1. Codificar: Permite convertir un archivo en una imagen de tamaño (indefinido x 1 pixel).",
    "2. Decodificar: Permite extraer el contenido de un archivo desde una imagen.",
    "Ingrese el nombre del archivo cuando se le solicite, y la ubicación donde desea guardar el resultado."
]

def render_multiline_text(texts, font, color, surface, x, y):
    """
    Renderiza texto multilínea en una superficie.
    """
    for i, line in enumerate(texts):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * font.get_linesize()))

# Variables de estado
input_active = False
user_text = ""
step = 0
selected_option = 0
mostrar_ayuda = False  # Estado para mostrar la ayuda

# Variables para almacenar datos ingresados por el usuario
archivo_codificar = ""
nombre_guardar = ""
archivo_decodificar = ""
output_file_path = ""

# Bucle principal
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            if mostrar_ayuda:
                # Si estamos en la pantalla de ayuda, manejar el clic en el botón "Volver"
                if button_volver_ayuda.collidepoint(e.pos):
                    mostrar_ayuda = False  # Ocultar ayuda y volver a la pantalla principal
            elif step == 0:
                # Manejar los clics en el menú principal
                if button_codificar.collidepoint(e.pos):
                    selected_option = 1
                    step = 1
                    user_text = ""
                elif button_decodificar.collidepoint(e.pos):
                    selected_option = 2
                    step = 1
                    user_text = ""
                elif button_ayuda.collidepoint(e.pos):
                    mostrar_ayuda = True  # Mostrar ayuda
            elif step > 0 and button_volver.collidepoint(e.pos):
                # Manejar el clic en el botón "Volver" durante el ingreso de datos
                step = 0
                selected_option = 0
                user_text = ""
        elif e.type == KEYDOWN:
            if input_active:
                if e.key == K_RETURN:
                    # Manejar el ingreso de datos y avanzar a la siguiente etapa
                    if step == 1:
                        if selected_option == 1:
                            archivo_codificar = user_text
                            user_text = ""
                            step = 2
                        elif selected_option == 2:
                            archivo_decodificar = user_text
                            user_text = ""
                            step = 2
                    elif step == 2:
                        if selected_option == 1:
                            nombre_guardar = user_text
                            crear_imagen(archivo_codificar, nombre_guardar)
                            user_text = ""
                            step = 0
                            selected_option = 0
                        elif selected_option == 2:
                            output_file_path = user_text
                            print(f"Decodificando {archivo_decodificar} y guardando resultado en {output_file_path}")
                            decodificar(archivo_decodificar, output_file_path)
                            user_text = ""
                            step = 0
                            selected_option = 0
                elif e.key == K_BACKSPACE:
                    # Manejar la eliminación de texto
                    user_text = user_text[:-1]
                else:
                    # Agregar texto ingresado por el usuario
                    user_text += e.unicode

    # Dibujar en la pantalla
    screen.fill(WHITE)

    if mostrar_ayuda:
        # Mostrar texto de ayuda en varias líneas
        render_multiline_text(ayuda_textos, font, BLACK, screen, 20, 20)
        # Dibujar el botón "Volver" en la pantalla de ayuda
        draw.rect(screen, GRAY, button_volver_ayuda)
        text_volver_ayuda = font.render('Volver', True, BLACK)
        screen.blit(text_volver_ayuda, (button_volver_ayuda.x + 75, button_volver_ayuda.y + 10))
    else:
        if step == 0:
            # Dibujar botones en el menú principal
            draw.rect(screen, RED, button_codificar)
            draw.rect(screen, GREEN, button_decodificar)
            draw.rect(screen, GRAY, button_ayuda)  # Botón de ayuda

            # Dibujar texto sobre los botones
            text_codificar = font.render('Codificar', True, BLACK)
            text_decodificar = font.render('Decodificar', True, BLACK)
            text_ayuda = font.render('Ayuda', True, BLACK)
            screen.blit(text_codificar, (button_codificar.x + 50, button_codificar.y + 10))
            screen.blit(text_decodificar, (button_decodificar.x + 40, button_decodificar.y + 10))
            screen.blit(text_ayuda, (button_ayuda.x + 20, button_ayuda.y + 10))
        else:
            input_active = True
            prompt_text = ""
            if step == 1:
                if selected_option == 1:
                    prompt_text = "Nombre del archivo a codificar + extension: "
                elif selected_option == 2:
                    prompt_text = "Nombre de la imagen a decodificar: "
            elif step == 2:
                if selected_option == 1:
                    prompt_text = "Nombre de la imagen a guardar: "
                elif selected_option == 2:
                    prompt_text = "Nombre del archivo resultante: "

            # Dibujar el texto de solicitud y el texto ingresado por el usuario
            prompt_surface = font.render(prompt_text, True, BLUE)
            user_text_surface = font.render(user_text, True, BLACK)
            screen.blit(prompt_surface, (50, 150))
            screen.blit(user_text_surface, (50, 200))

            # Dibujar el cuadro resaltado para la entrada de texto
            input_box = Rect(45, 195, 510, 40)
            draw.rect(screen, ACTIVE_COLOR, input_box, 2)

            # Dibujar el botón "Volver" durante el ingreso de datos
            draw.rect(screen, GRAY, button_volver)
            text_volver = font.render('Volver', True, BLACK)
            screen.blit(text_volver, (button_volver.x + 75, button_volver.y + 10))

    # Actualizar la pantalla
    display.flip()

# Salir de Pygame
quit()