"""Resultados de referencia de las dos entregas sinteticas de la sesion 07."""
from decimal import Decimal

ESPERADO = {
    '2026-10-06': [
        ('P01', 'Seguro Auto Demo', 4, 3, 3, 3700, Decimal('1233.33'), 1000, 1500, 3, 1, 800),
        ('P02', 'Seguro Salud Demo', 4, 3, 4, 4000, 1000, 800, 1200, 2, 0, 600),
        ('P03', 'Seguro Hogar Demo', 3, 3, 3, 2200, Decimal('733.33'), 600, 900, 3, 0, 400),
        ('P99', 'SIN_CATALOGO', 1, 1, 1, 500, 500, 500, 500, 0, 0, 0),
    ],
    '2026-10-07': [
        ('P01', 'Seguro Auto Demo', 4, 3, 4, 4900, 1225, 1000, 1600, 3, 0, 1000),
        ('P02', 'Seguro Salud Demo', 4, 3, 4, 4200, 1050, 800, 1400, 2, 0, 500),
        ('P03', 'Seguro Hogar Integral Demo', 4, 4, 4, 3400, 850, 600, 1200, 5, 0, 950),
        ('P99', 'SIN_CATALOGO', 1, 1, 1, 500, 500, 500, 500, 0, 0, 0),
    ],
}
