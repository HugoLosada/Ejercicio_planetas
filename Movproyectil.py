""" 
Este programa es un simulador de movimiento de proyectiles, 
El usuario puede ingresar parámetros como la velocidad inicial, el ángulo de lanzamiento y la aceleracion de la gravedad para simular el movimiento de múltiples proyectiles
"""

#Importamos las librerias necesarias para cálculas, para poder representar las gráficas y para poder hacer la interfaz.
import math
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import tkinter as tk

"""
Creamo la clase projectile que representa un projectil con: 
su velocidad inicial, ángulo de lanzamiento y gravedad. 
La velocidad inicial y la gravedad se almacenan directamente,
mientras que el ángulo de lanzamiento se convierte de grados a radianes usando la función math.radians()
"""

class Projectile:
    def __init__(self, initial_velocity, launch_angle, gravity):
        self.initial_velocity = initial_velocity
        self.launch_angle = math.radians(launch_angle)
        self.gravity = gravity

"""
Creamos la clase ProjectileSimulator que representa la interfaz gráfica de usuario para simular el movimiento de proyectiles
Utilizamos variables de cadena para almacenar la elección del sistema de unidades, el número de proyectiles y los resultados.
"""

class ProjectileSimulatorGUI:
    def __init__(self, root):
        self.root = root
#Con .title le introducimos el título que queramos que tenga 
        self.root.title("Projectile Motion Simulator")
# La variable self.unit_system_var se asocia con el campo de entrada donde el usuario puede ingresar el sistema de unidades (SI o US).
        self.unit_system_var = StringVar()
#Esta variable se asocia con el número de proyectiles que introduce el usuario 
        self.num_projectiles_var = StringVar()
#Esta variable se utiiza para mostrar los resultados de la simulación en un texto de la interfaz
        self.results_text_var = StringVar()

        self.create_widgets()

#Con esta funcion creamos botones, etiquetas... para la interfaz 
#Los widgets permiten al usuario ingresar la unidad del sistema, el número de proyectiles y simular el movimiento de los proyectiles.

    def create_widgets(self):
        Label(self.root, text="Choose unit system (SI or US):").grid(row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.unit_system_var).grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="Enter the number of projectiles:").grid(row=1, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.num_projectiles_var).grid(row=1, column=1, padx=10, pady=10)

        Button(self.root, text="Simulate", command=self.simulate_projectiles).grid(row=2, column=0, columnspan=2, pady=20)

        Label(self.root, text="Results:").grid(row=3, column=0, columnspan=2, pady=10)
        Label(self.root, textvariable=self.results_text_var).grid(row=4, column=0, columnspan=2, pady=10)

#Con esta función realizamos la simulación para los distintos proyectiles 

    def simulate_projectiles(self):
        unit_system = self.unit_system_var.get().upper()
        num_projectiles = int(self.num_projectiles_var.get())

        projectiles = []
        results_list = []  # Guardamos los resultados 

        for i in range(num_projectiles):
            try:
                initial_velocity = float(input(f"Enter initial velocity ({get_velocity_unit(unit_system)}): "))
                launch_angle = float(input("Enter launch angle in degrees: "))
                gravity = float(input(f"Enter gravitational acceleration ({get_gravity_unit(unit_system)}): "))
                projectiles.append(Projectile(initial_velocity, launch_angle, gravity))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
                return

# Calcula y representa gráficamente la trayectoria de cada proyectil. También acumula información de resultados 

        for i, projectile in enumerate(projectiles, start=1):
            x_points, y_points, time_of_flight, max_height, range_val = self.calculate_trajectory(projectile)

            plt.plot(x_points, y_points, label=f"Projectile {i}")

            results_text = (
                f"Projectile {i} - Time of Flight: {time_of_flight} {get_time_unit(unit_system)}, "
                f"Max Height: {max_height} {get_length_unit(unit_system)}, Range: {range_val} {get_length_unit(unit_system)}"
            )

            results_list.append(results_text)

#Configura y muestra el gráfico de las trayectorias de los proyectiles utilizando Matplotlib. 
# Luego, muestra información adicional sobre los proyectiles en una nueva ventana.
        self.results_text_var.set("\n".join(results_list))

        plt.title("Projectile Motion")
        plt.xlabel(f"Horizontal Distance ({get_length_unit(unit_system)})")
        plt.ylabel(f"Vertical Distance ({get_length_unit(unit_system)})")
        plt.legend()

        # Show the plot in a new window
        plt.show()

        # After showing the plot, display additional information
        self.show_additional_info(projectiles, unit_system)

#Calcula la trayectoria de un proyectil  utilizando las ecuaciones del movimiento parabólico. 
#Devuelve los  puntos x e y, el tiempo de vuelo, la altura máxima y el alcance.

    def calculate_trajectory(self, projectile):
        time_of_flight = (2 * projectile.initial_velocity * math.sin(projectile.launch_angle)) / projectile.gravity
        max_height = (projectile.initial_velocity**2 * (math.sin(projectile.launch_angle))**2) / (2 * projectile.gravity)
        range_val = (projectile.initial_velocity**2 * math.sin(2 * projectile.launch_angle)) / projectile.gravity

        time_points = [i * 0.1 for i in range(int(time_of_flight * 10) + 1)]
        x_points = [projectile.initial_velocity * math.cos(projectile.launch_angle) * t for t in time_points]
        y_points = [
            projectile.initial_velocity * math.sin(projectile.launch_angle) * t - 0.5 * projectile.gravity * t**2
            for t in time_points
        ]

        return x_points, y_points, time_of_flight, max_height, range_val

#Esta función muesstra información adicional sobre cada proyectil en una nueva ventana

    def show_additional_info(self, projectiles, unit_system):
        # Create a new window for additional information
        info_window = tk.Toplevel(self.root)
        info_window.title("Projectile Information")

        # Esta línea de código utiliza un bucle for y la función enumerate para iterar sobre la lista de proyectiles
        for i, projectile in enumerate(projectiles, start=1):
            #[2:] se utiliza para desempaquetar solo los elementos desde el tercer elemento en adelante de esa tupla.
            time_of_flight, max_height, range_val = self.calculate_trajectory(projectile)[2:]
#Este  código crea una etiqueta para mostrar información sobre los proyectiles 
            info_label = Label(info_window, text=(
                f"Projectile {i} Information:\n"
                f"Time of Flight: {time_of_flight} {get_time_unit(unit_system)}\n"
                f"Max Height: {max_height} {get_length_unit(unit_system)}\n"
                f"Range: {range_val} {get_length_unit(unit_system)}"
            ))
            info_label.pack(pady=10)


# Estas funciones toman el sistema de unidades (unit_system) como parámetro y devuelven la unidad correspondiente en función de ese sistema

def get_velocity_unit(unit_system):
    """Get the velocity unit based on the unit system."""
    return "m/s" if unit_system == "SI" else "ft/s"

def get_gravity_unit(unit_system):
    """Get the gravity unit based on the unit system."""
    return "m/s^2" if unit_system == "SI" else "ft/s^2"

def get_time_unit(unit_system):
    """Get the time unit based on the unit system."""
    return "s" if unit_system == "SI" else "s"

def get_length_unit(unit_system):
    """Get the length unit based on the unit system."""
    return "m" if unit_system == "SI" else "ft"


#Esta parte del código determina si el script se está ejecutando como un programa independiente o si está siendo importado como un módulo en otro script.

if __name__ == "__main__":
    root = Tk()
    app = ProjectileSimulatorGUI(root)
    root.mainloop()