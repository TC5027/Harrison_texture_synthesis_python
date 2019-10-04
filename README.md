# Harrison_texture_synthesis_python
Python implementation of the Harrison's algorithm for texture synthesis

<p align="center"><img alt="texture1" src="https://github.com/TC5027/Harrison_texture_synthesis_python/blob/master/inputs/texture1.jpg"></p>
<p align="center"><img alt="texture1" src="https://github.com/TC5027/Harrison_texture_synthesis_python/blob/master/outputs/output1.jpg"></p>


<p align="center"><img alt="texture1" src="https://github.com/TC5027/Harrison_texture_synthesis_python/blob/master/inputs/texture2.jpg"></p>
<p align="center"><img alt="texture1" src="https://github.com/TC5027/Harrison_texture_synthesis_python/blob/master/outputs/output2.jpg"></p>

<p align="center"><img alt="texture1" src="https://github.com/TC5027/Harrison_texture_synthesis_python/blob/master/inputs/texture3.jpg"></p>
<p align="center"><img alt="texture1" src="https://github.com/TC5027/Harrison_texture_synthesis_python/blob/master/outputs/output3.jpg"></p>

## Sources

L'algorithme peut etre trouvé dans le document dissertation.pdf disponible sur le site de Dr. Paul Harrison http://www.logarithmic.net/pfh/.

## Exemple d'utilisation

La commande pour se servir de cet outil est de la forme "./Synthesis.py <fichier_input.jpg> <fichier_output.jpg> N M dispersion etapes" avec dans l'ordre:

N : le nombre de voisins analysés pour la synthèse d'un pixel (4)

M : le nombre de candidats pris aléatoirement pour la synthèse d'un pixel (3)

dispersion : paramètre pondérant la metric (30)

etapes : le nombre d'étapes par lequel l'algorithme va passer avant de rendre l'output (4)



(entre parentheses valeurs que j'ai personnellement pu utilisées)
Pour plus d'explications je renvoie à la lecture du document de monsieur Harrison.
