"""---"""
from os import system

from ecomm import Postgres
from pandas import DataFrame
from print_cores import Cores

QUERY = '''
SELECT
    *
FROM "ECOMM".ml_venda
WHERE id = '%s'
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
    return df_aux.rename({
        'created':'data_criacao_venda',
        'cancelled':'data_cancelamento',
        'ready_to_print':'data_impressao',
        'ready_to_ship':'data_pronto_enviar',
        'shipped':'data_envio'}, axis=0)


if __name__ == '__main__':
    system('cls')
    while True:
        cod = input('\nDigite o id_venda (Codigo da venda MercadoLivre): ').strip()
        if cod.isnumeric():
            # result = re(QUERY, cod).to_json()
            # parsed = loads(result)
            # print(dumps(parsed, indent=4))
            try:
                result = re(QUERY, cod)
                if not result.empty:
                    print(f'\nID digitado = {Cores.VERDE_CLARO}{cod}{Cores.RESET}')
                    print(f'\n{Cores.AZUL_CLARO}Resultados:\n\n{Cores.RESET}', re(QUERY, cod))
                else:
                    print('\nNao tem dado.')
            except KeyError:
                print(f'\n{Cores.VERMELHO_CLARO}Nao existe o ID.{Cores.RESET}')
            input(f'\n{Cores.AMARELO}Pressione qualquer tecla para continuar...{Cores.RESET}')

        system('cls')
