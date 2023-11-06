from math import sin
import numpy as np

def bezier_curve(p0, p1, p2, t):
			"""
			Calcule un point sur une courbe de Bézier quadratique.
			
			:param p0: Premier point de contrôle (tuple de coordonnées).
			:param p1: Deuxième point de contrôle (tuple de coordonnées).
			:param p2: Troisième point de contrôle (tuple de coordonnées).
			:param t: Paramètre de la courbe (0 <= t <= 1).
			:return: Tuple représentant les coordonnées du point sur la courbe.
			"""
			x = int(round((1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]))
			y = int(round((1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
			return x, y

def trace_courbe_bezier(p0, p1, p2):
	"""
	Trace une courbe de Bézier quadratique complète.
	
	:param p0: Premier point de contrôle (tuple de coordonnées).
	:param p1: Deuxième point de contrôle (tuple de coordonnées).
	:param p2: Troisième point de contrôle (tuple de coordonnées).
	:return: Liste des points (tuples de coordonnées) formant la courbe.
	"""
	return [bezier_curve(p0, p1, p2, t) for t in np.linspace(0, 1, 100)]

def ondulation(courbe, amplitude=9, frequence=0.2):
	"""
	Ajoute une ondulation à une courbe.
	
	:param courbe: Liste des points (tuples de coordonnées) de la courbe originale.
	:param amplitude: Amplitude de l'ondulation (valeur par défaut : 9).
	:param frequence: Fréquence de l'ondulation (valeur par défaut : 0.2).
	:return: Liste des points (tuples de coordonnées) de la courbe ondulée.
	"""
	return [(x, int(y + amplitude * sin(frequence * x))) for x, y in courbe]


def add_points(courbe):
	"""
	Ajoute des points intermédiaires dans une courbe pour la rendre plus lisse.
	
	:param courbe: Liste des points (tuples de coordonnées) de la courbe originale.
	:return: Liste des points (tuples de coordonnées) de la courbe avec points ajoutés.
	"""
	
	new_courbe = [courbe[0]]
	for i in range(1, len(courbe)):
		previous_point  = courbe[i - 1]
		current_point  = courbe[i]
		
		x = (previous_point[0] + current_point[0]) // 2
		y = (previous_point[1] + current_point[1]) // 2
		mid_point = (x, y)
		
		new_courbe.extend([mid_point, current_point])

	return new_courbe



def smooth_around_line(terrain, ligne, depth=4):
		"""
		Lisse un terrain autour d'une ligne spécifiée.
		
		:param terrain: Tableau représentant le terrain.
		:param ligne: Liste de tuples de coordonnées représentant la ligne.
		:param depth: Profondeur du lissage.
		:return: Tableau du terrain lissé.
		"""
		smoothed_terrain = terrain.copy()
		
		for x, y in ligne:
			for dx in range(-depth, depth+1):
				for dy in range(-depth, depth+1):
					dist = np.sqrt(dx*dx + dy*dy)
				
					xi, yi = x + dx, y + dy
					if 0 <= xi < terrain.shape[0] and 0 <= yi < terrain.shape[1]:
						factor = (dist / depth)**2
						smoothed_terrain[xi, yi] = min(smoothed_terrain[xi, yi], terrain[xi, yi] * factor)
		
		return smoothed_terrain

def int_lerp(a, b, t):
	"""
	Interpolation linéaire entre deux valeurs entières.
	
	:param a: Valeur de départ.
	:param b: Valeur de fin.
	:param t: Paramètre d'interpolation (0 <= t <= 1).
	:return: Valeur interpolée.
	"""
	return int(a + (b - a) * t)

def bezier_cubic_curve(start, c1, c2, end, t):
	"""
	Calcule un point sur une courbe de Bézier cubique.
	
	:param start: Point de départ de la courbe (tuple de coordonnées).
	:param c1: Premier point de contrôle (tuple de coordonnées).
	:param c2: Deuxième point de contrôle (tuple de coordonnées).
	:param end: Point de fin de la courbe (tuple de coordonnées).
	:param t: Paramètre de la courbe (0 <= t <= 1).
	:return: Tuple représentant les coordonnées du point sur la courbe.
	"""
	x = int_lerp(
			int_lerp(
				int_lerp(start[0], c1[0], t), 
				int_lerp(c1[0] , c2[0], t),
				t), 
			int_lerp(
				int_lerp(c1[0] , c2[0], t), 
				int_lerp(c2[0] , end[0], t),
				t),
		t)
	y = int_lerp(
			int_lerp(
				int_lerp(start[1], c1[1], t), 
				int_lerp(c1[1] , c2[1], t),
				t), 
			int_lerp(
				int_lerp(c1[1] , c2[1], t), 
				int_lerp(c2[1] , end[1], t),
				t),
		t)
	return x, y

def trace_courbe_cubic_bezier(p0, p1, p2, p3):
	"""
	Trace une courbe de Bézier cubique complète.
	
	:param p0: Premier point de contrôle (tuple de coordonnées).
	:param p1: Deuxième point de contrôle (tuple de coordonnées).
	:param p2: Troisième point de contrôle (tuple de coordonnées).
	:param p3: Quatrième point de contrôle (tuple de coordonnées).
	:return: Liste des points (tuples de coordonnées) formant la courbe.
	"""
	return [bezier_cubic_curve(p0, p1, p2, p3, t) for t in np.linspace(0, 1, 100)]