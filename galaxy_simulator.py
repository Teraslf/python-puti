import tkinter as tk
from random import randint, uniform, random
import math

#Шкала (диаметр радиопузыря) в световых годах:
SCALE = 225 #Ввести 225, чтобы увидеть радиопузырь Земли

#Число развитых цивилизаций из уравнения Дрейка:
NUM_CIVS = 15600000

root = tk.Tk()
root.title("Галактика Млечного Пути")
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

#Фактические размеры Млечного Пути(св годы)
DISC_RADIUS = 50000
DISC_HEIGHT = 1000
DISC_VOL = math.pi * DISC_RADIUS**2 * DISC_HEIGHT

def scale_galaxy():
    """ Шкалирование размеров галактики на основе
    размера радиопузыря (scale) ."""
    disc_radius_scaled = round(DISC_RADIUS / SCALE)
    bubble_vol = 4/3 * math.pi * (SCALE / 2)**3
    disc_vol_scaled = DISC_VOL/bubble_vol
    return disc_radius_scaled, disc_vol_scaled

def detect_prob(disc_vol_scaled):
#Вычислить вероятность, что галактические цивилизации обнаружат друг друга.
# отношение цивилизаций к шкалированному объему галактики
    ratio = NUM_CIVS / disc_vol_scaled
    if ratio < 0.002: # установить очень низкие соотношения
        detection_prob = 1 # равными единичной вероятности
    else:
        detection_prob = -0.004757 * ratio**4 + \
                          0.06681 * ratio**3 - 0.3605 * \
                          ratio**2 + 0.9215 * ratio + 0.00826
    return round(detection_prob, 3)

def random_polar_coordinates(disc_radius_scaled):
#Сгенерировать случайную (х, у) внутри диска из равномерного распределения для 2-мерного изображения.
    r = random()
    theta = uniform(0, 2 * math.pi)
    x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
    y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
    return x, y

def spirals(b, r, rot_fac, fuz_fac, arm):
    """Построить спиральные рукава для изображения в tkinter,
        используя формулу логарифмической спирали.

    b - произвольная константа в уравнении логарифмической спирали
    r - радиус прошкалированного галактического диска
    rot_fac - коэффициент поворота
    fuz_fac - случайный сдвиг в позиции звезды в рукаве,
    применительно к переменной 'fuzz'
    arm - рукав спирали (0 - главный рукав, 1 - замыкающие звезды)
    """
    spiral_stars = []
    fuzz = int(0.030 * abs(r)) #случайно сдвинуть местоположения звезд
    theta_max_degrees = 520
    for i in range(theta_max_degrees): #range(0, 600, 2) не для черной дыры
        theta = math.radians(i)
        x = r * math.exp(b * theta) * math.cos(theta + \
            math.pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
        y = r * math.exp(b * theta) * math.sin(theta + math.pi * \
            rot_fac) + randint(-fuzz, fuzz) * fuz_fac
        spiral_stars.append((x, y))
    for x, y in spiral_stars:
        if arm == 0 and int (x % 2) == 0:
            c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='')
        elif arm == 0 and int(x % 2) != 0:
            c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
        elif arm == 1:
            c.create_oval(x, y, x, y, fill='white', outline='')

def star_haze(disc_radius_scaled, density):
    """Случайно распределите тусклые звезды в галактическом диске.
    disc_radius_scaled = радиус галактического диска,
    прошкалированный в плотность радиопузыря
    density = множитель для варьирования числа размещенных звезд
    """

    for i in range(0, disc_radius_scaled * density):
        x, y = random_polar_coordinates(disc_radius_scaled)
        c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')

def main():
    """Рассчитать вероятность обнаружения и изобразить
        галактику и статистику."""
    disc_radius_scaled, disc_vol_scaled = scale_galaxy()
    detection_prob = detect_prob(disc_vol_scaled)

    # построить 4 основных спиральных рукава и 4 тянущихся позади рукава
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-2.09, fuz_fac=1.5, arm=1)

    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
    star_haze(disc_radius_scaled, density=8)

    # изобразить легенду
    c.create_text(-455, -360, fill='white', anchor='w', text='Один пиксел = {} св. лет'.format(SCALE))
    c.create_text(-455, -330, fill='white', anchor='w', text='Диаметр радиопузыря = {} св. лет'.format(SCALE))
    c.create_text(-455, -300, fill='white', anchor='w', text='Вероятность обнаружения для {:,} цивилизаций = {}'.format(NUM_CIVS, detection_prob))
    # разместить пузырь Земли диаметром 225 св. лет и аннотировать 0
    if SCALE == 225:
        c.create_rectangle(115, 75, 116, 76, fill='red', outline='')
        c.create_text(118, 72, fill='red', anchor='w', text="<----------Радиопузырь Земли")

    # запустить цикл tkinter
    root.mainloop()
if __name__ == '__main__' :
    main()
    print()
