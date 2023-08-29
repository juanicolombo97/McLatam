from BANCO_MUNDIAL import scraper_banco_mundial
from ComunidadAndina import scraper_comunidad_andina
from CAF import scraper_CAF
from FONPLATA import scraper_fonplata
from NUG import scraper_naciones_unidas_global
from OEA import scraper_oea
from Procurement import scraper_procurement_notices


def main():
    print("Ejecutando el archivo principal")
    scraper_oea.main()
    scraper_banco_mundial.main()
    scraper_comunidad_andina.main()
    scraper_CAF.main()
    scraper_fonplata.main()
    scraper_naciones_unidas_global.main()
    scraper_procurement_notices.main()


if __name__ == "__main__":
    main()
