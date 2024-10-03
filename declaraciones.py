from PIL import Image
from copy import deepcopy

ob0 = '00000000'
ob1 = '00000001'
ob2 = '00000010'
ob3 = '00000011'
ob4 = '00000100'

"""
Conversor de archivos a imagen

PROBLEMAS:  
        1-La creacion de la imagen no es correcta

Pasos:
(yasta) 1- Pasar el archivo a binario y guardarlo en una lista tipo: info, pixeles en blanco, cantidad de pixeles en blanco(terminado) y extension de archivo, ej:"zip"
(yasta) 2- Hacer grupos de 3 bytes(RGB) 
        3- Crear una imagen de mapa de bits (.png) 
Mitigacion de errores: 
    La imagen sea de un Ancho x Alto de {Indefinidos_pixeles x 1pixel} - Para evitar la edicion e implementacion de ceros para que pueda caber en la imagen
    Que el ultimo byte(B) sea ob0 - En el caso de que no hayan la cantidad de bytes exactos con multiplos 3 

A tener en cuenta:
    1 bit -> 1 u 0 -> 2 posibilidades
    1 byte -> 8 bits -> 11111111 - ob0-> 255 posibilidades(colores)
"""




def file_to_nested_bit_list(file_path : str):
    """_summary_

    Args:
        file_path (str): La ruta del archivo a codificar

    Raises:
        ValueError: Si la extension del archivo no es apta para la decodificacion, lanza un error
        ValueError: Este segundo ValueError es de decoracion :v
        ValueError: Igual que el primer ValueError, no deberia aparecer ya que al raisear el primer error se detiene el programa

    Returns:
        lista: Devuelve toda la lista 
    """

    # Obtén la extensión del archivo
    # Usamos rsplit para dividir desde el final y tomamos la última parte después del último punto
    extension_archivo_str = file_path.rsplit('.', 1)[-1]

    extension_archivo = [format(ord(caracter), '08b') for caracter in extension_archivo_str]
    if len(extension_archivo) <= 4:
        pass
    else:
        raise ValueError("La extension del archivo debe ser de 4 letras o menor")

    # lee el archivo
    with open(file_path, 'rb') as file:  
        binary_content = file.read() #Nos da la info del archivo en hexadecimal 
    
    # Convierte cada byte hexadecimal a su representación binaria
    bit_list = [format(byte, '08b') for byte in binary_content]
    
    # Divide la lista de bits en sublistas de 3 elementos
    nested_bit_list = [bit_list[i:i + 3] for i in range(0, len(bit_list), 3)]
    
    # Detectar si la última sublista tiene 2 o 1 elementos
    last_sublist = nested_bit_list[-1] # ultima sublista
    if len(nested_bit_list) > 0: #Asegurador, este condicional añade la cantidad de bytes necesarias y el contador        
        if len(last_sublist) == 0 or len(last_sublist) == 3:
            nby = ob0 #0
        elif len(last_sublist) == 2:
            nby = ob1 #1
            last_sublist.append(ob0)
        elif len(last_sublist) == 1:
            nby = ob2 #2
            last_sublist.append(ob0)
            last_sublist.append(ob0)
        else:
            raise ValueError("Imposible que arroje este error...")
        
    if len(extension_archivo) > 0:  #Asegurador, este condicional añade la cantidad de caracteres que tiene la extension
        if len(extension_archivo) == 1:
            Ccext = ob1 #1
            extension_archivo.append(ob1)
            extension_archivo.append(ob0)
        elif len(extension_archivo) == 2:
            Ccext = ob2 #2
            extension_archivo.append(ob0)
        elif len(extension_archivo) == 3:
            Ccext = ob3 #3
        elif len(extension_archivo) == 4: 
            Ccext = ob4 #4
        else:
            raise ValueError("Asegurese que la extension tiene entre 1-4 caracteres")
    
    # Añadir metadatos
    #Extension del archivo : Ccext
    #La siguiente pieza de codigo puede ser consultada en el papel de calculo 
    extension_metadata = [Ccext, nby, ob0]
    if len(extension_archivo) < 4:
        nested_bit_list.append(extension_archivo)
        nested_bit_list.append(extension_metadata)
    elif len(extension_archivo) == 4:
        nested_bit_list.append(extension_archivo[:3])
        extension_metadata.pop(2)
        extension_metadata.reverse()
        extension_metadata.append(extension_archivo[3])
        extension_metadata.reverse()
        nested_bit_list.append(extension_metadata)
    return nested_bit_list

def crear_imagen(file_path, new_file_name):
    """_summary_

    Args:
        file_path (str): Nombre del archivo a codificar, solo toma el nombre del archivo
        new_file_name (_type_): Nombre de la imagen 
    """
    bytes_list = file_to_nested_bit_list(file_path) #Saca la lista de bytes(está dividida en 3 sublistas)
    int_list = [[int(bin_str, 2) for bin_str in sublist] for sublist in bytes_list] #Pasa los bytes a int

    # Determinar dimensiones de la imagen
    flat_pixel_values = [item for sublist in int_list for item in sublist] # Elimina las sublistas
    width = len(flat_pixel_values) // 3  # Ancho de la imagen, Cada píxel tiene 3 valores (RGB)
    height = 1 #Altura de la imagen, 1 pixel

    image = Image.new('RGB', (width, height)) #Crea una imagen en blanco con 

    
    for x in range(width): # Itera sobre cada píxel en la primera fila (y solo en esa fila)
        # Obtiene los valores de color de la lista plana de valores de píxeles
        r = flat_pixel_values[x * 3] #Rojo
        g = flat_pixel_values[x * 3 + 1] #Verde
        b = flat_pixel_values[x * 3 + 2] #Azul
        image.putpixel((x, 0), (r, g, b)) # Coloca el color del píxel en la posición (x, 0) en la imagen

    image.save(new_file_name + '.png') #Guarda la imagen en un archivo de mapa de bits(.png) cuyo nombre es el nombre de la imagen(obviamente)






############################################################################ Lo de arriba es para codificar
############################################################################
############################################################################ Lo de abajo es para decodificar





def lista_a_archivo(IDAT, ext_len, padding, output_file_path):

    ultima_sublista = IDAT[-1][-1]
    penultima_sublista = IDAT[-1][-2]

    if ext_len == 4:
        # Hacer una copia profunda de IDAT para no afectar la lista original
        copied_IDAT = deepcopy(IDAT)
        # Acceder a las sublistas en la copia
        ultima_sublista = copied_IDAT[-1][-1]  # Última sublista
        extension = copied_IDAT[-1][-2]  # Penúltima sublista
        # Añadir el primer elemento de la última sublista a la penúltima sublista
        extension.append(ultima_sublista[0])
        # Pasa la extension binaria a str
        extesion_archivo = ''.join([chr(int(b, 2)) for b in extension]) 
    elif ext_len == 3:
        # Pasa la extension binaria a str
        extesion_archivo = ''.join([chr(int(b, 2)) for b in penultima_sublista]) 
    elif ext_len == 2:
        extension = penultima_sublista[0:2]
        # Pasa la extension binaria a str
        extesion_archivo = ''.join([chr(int(b, 2)) for b in extension])
    elif ext_len == 1:
        extension = penultima_sublista[0:1]
        # Pasa la extension binaria a str
        extesion_archivo = ''.join([chr(int(b, 2)) for b in extension])
    else:
        print("Hubo un error en la decodificacion de la extension")
        pass
    
    if padding == 0:
        info = IDAT[0][:-2] # Obtiene toda la información de IDAT excepto los últimos 2 bytes
    elif padding == 1:
        info = IDAT[0]# Obtiene la información completa de IDAT
        # Elimina los dos últimos elementos de la lista
        info.pop(-1)
        info.pop(-1)
        info[-1].pop(-1)# Elimina el último elemento de la ultima sublista apodada 'info'
    elif padding == 2:
        info = IDAT[0]# Obtiene la información completa de IDAT
        # Elimina los dos últimos elementos de la lista
        info.pop(-1)
        info.pop(-1)
        # Elimina los dos últimos elementos del último sublistado de 'info'
        info[-1].pop(-1)
        info[-1].pop(-1)
    else:
        raise ValueError("Ocurrió un error, vuelva a intentarlo")
    
    # Convertir las cadenas de bits a bytes y almacenar en un bytearray
    info = [info]
    # Convertir las cadenas de bits a bytes y almacenar en un bytearray
    datos_binarios = bytearray()
    for sublista in info:
        for subsublista in sublista:
            for b in subsublista:
                byte_valor = int(b, 2)  # Convertir binario a entero
                datos_binarios.append(byte_valor)  # Añadir a bytearray


    # Escribir datos binarios en un archivo
    with open(output_file_path + '.' + extesion_archivo, 'wb') as archivo:
        archivo.write(datos_binarios)

def decodificar(image_path, output_file_path):
    # Open the image
    imagen = Image.open(image_path + '.png')
    # Get image dimensions
    anchura, altura = imagen.size
    # Get pixel data and convert to list of lists
    pixeles = list(imagen.getdata())
    pixeles = [list(pixel) for pixel in pixeles]
    pixeles_sublistas = [pixeles[i * anchura:(i + 1) * anchura] for i in range(altura)]

    IDAT = []
    for fila in pixeles_sublistas:
        fila_bits = []
        for pixel in fila:
            pixel_bits = [format(componente, '08b') for componente in pixel]
            fila_bits.append(pixel_bits)
        IDAT.append(fila_bits)

    ultima_sublista = IDAT[-1][-1]
    ext_len = 0
    padding = 0
    
    if ultima_sublista[-1] == ob2 and ultima_sublista[-2] == ob4:
        ext_len = 4
        padding = 2
    elif ultima_sublista[-1] == ob1 and ultima_sublista[-2] == ob4:
        ext_len = 4
        padding = 1
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob4:
        ext_len = 4
        padding = 0
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob2 and ultima_sublista[-3] == ob3:
        ext_len = 3
        padding = 2
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob1 and ultima_sublista[-3] == ob3:
        ext_len = 3
        padding = 1
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob0 and ultima_sublista[-3] == ob3:
        ext_len = 3
        padding = 0
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob2 and ultima_sublista[-3] == ob2:
        ext_len = 2
        padding = 2
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob1 and ultima_sublista[-3] == ob2:
        ext_len = 2
        padding = 1
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob0 and ultima_sublista[-3] == ob2:
        ext_len = 2
        padding = 0
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob2 and ultima_sublista[-3] == ob1:
        ext_len = 1
        padding = 2
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob1 and ultima_sublista[-3] == ob1:
        ext_len = 1
        padding = 1
    elif ultima_sublista[-1] == ob0 and ultima_sublista[-2] == ob0 and ultima_sublista[-3] == ob1:
        ext_len = 1
        padding = 0
    else:
        ext_len = 3
        padding = 0

    lista_a_archivo(IDAT, ext_len, padding, output_file_path)