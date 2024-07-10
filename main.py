"""---"""
from os import system

from ecomm import Postgres
from pandas import DataFrame
from psycopg import OperationalError
from rich import print as pprint

QUERY = '''
SELECT ml_venda.id as codigo_venda,
	ml_venda.created as data_criacao_venda,
	ml_venda.cancelled as data_cancelamento,
	ml_venda.ready_to_print as data_impressao,
	ml_venda.ready_to_ship as data_pronto_enviar,
	ml_venda.shipped as data_envio,
	ml_pedido.pedido_sep as numero_pedido_separacao,
	ml_pedido.pedido_cliente as numero_pedido_cliente,
	ml_pedido.nota_cliente,
	ml_pedido.created as data_pedido_cliente,
	ml_pedido.entrada as data_entrada_cd,
	CASE
		WHEN ml_pedido.cd_loja = '01' THEN 'CD'
		WHEN ml_pedido.cd_loja = '03' THEN 'ASA NORTE'
		WHEN ml_pedido.cd_loja = '04' THEN 'CEILANDIA'
		WHEN ml_pedido.cd_loja = '05' THEN 'GAMA'
		WHEN ml_pedido.cd_loja = '06' THEN 'SOF SUL'
		WHEN ml_pedido.cd_loja = '07' THEN 'PLANALTINA'
		ELSE null
	END as loja_vl
FROM "ECOMM".ml_venda
INNER JOIN "ECOMM".ml_pedido
ON ml_venda.id = ml_pedido.id
WHERE ml_venda.id = '%s'
'''

def re(query:str, order_id:str) -> DataFrame:
    """_summary_

    Args:
        query (str): Consulta a tabela "ECOMM".ml_venda.
        order_id (str): ID da venda MercadoLivre.

    Returns:
        DataFrame: Dataframe com o resultado da consulta.
    """

    with Postgres() as db:
        df_db = db.query(query%order_id)
        df_aux = df_db.loc[0].copy()
    return df_aux


if __name__ == '__main__':
    system('cls')
    while True:
        cod: str = input('\nDigite o id_venda (Codigo da venda MercadoLivre): ').strip()
        if cod.isnumeric():
            try:
                df_result: DataFrame = re(QUERY, cod)
                if not df_result.empty:
                    pprint(f'\nID digitado = [green]{cod}[/green]')
                    pprint('\n[dodger_blue1]Resultados:[/dodger_blue1]\n\n')
                    pprint(df_result)

                else:
                    pprint('\n[bright_yellow]Nao tem dado.[/bright_yellow]')

            except KeyError:
                pprint('\n[bright_yellow]Nao existe o ID.[/bright_yellow]')

            except OperationalError as e:
                pprint(
                    '\n[bright_yellow]Opa, erro na conexao com o bando de dados ![/bright_yellow]')
                input(
                    '\nPressione qualquer tecla para sair...')
                raise ValueError() from e

            input(
                '\nPressione qualquer tecla para continuar...')

        system('cls')
