import pandas as pd


def criar_arquivo_ibge_nomes():
    df_ini = pd.read_csv('nomes-censos-ibge.csv', header=0, na_values=0)

    df_ini = df_ini.rename({'Nome': 'nome'}, axis=1)
    df_ini['nome'] = df_ini['nome'].str.lower()
    df_ini['id'] = pd.Series(pd.RangeIndex(1, len(df_ini) + 1, 1))
    df_ini = df_ini.fillna(0)
    df_ini = df_ini[['id', 'nome', 'ate1930', 'ate1940', 'ate1950', 'ate1960', 'ate1970', 'ate1980', 'ate1990',
                     'ate2000', 'ate2010']].astype('int64', errors='ignore')
    df_ini.to_csv('novos_arquivos_csv/nomes_censos_ibge_novo.csv', index=0)

    df_id = df_ini[['id', 'ate1930', 'ate1940', 'ate1950', 'ate1960', 'ate1970', 'ate1980', 'ate1990', 'ate2000',
                    'ate2010']].astype('int64', errors='ignore')

    df_id = df_id.rename({'id': 'nome_id'}, axis=1)
    df_id.to_csv('novos_arquivos_csv/ibge_quantidades.csv', index=0)

    df_nomes = df_ini[['id', 'nome']]
    df_nomes.to_csv('novos_arquivos_csv/ibge_nomes.csv', index=0)


def criar_arquivo_rank():
    df_ini = pd.read_csv('novos_arquivos_csv/nomes_censos_ibge_novo.csv', header=0, na_values=0)
    df_nome = pd.read_csv('novos_arquivos_csv/ibge_nomes.csv', header=0, na_values=0)
    df_end = df_nome['id']

    for decada in range(1930, 2020, 10):
        col = 'ate%d' % decada
        rank = 'rank%d' % decada

        df_decada = df_ini[['id', col]]
        df_decada = df_decada.dropna()

        df_decada[rank] = df_decada[col].rank(ascending=0, method='dense')
        df_end = pd.merge(df_end, df_decada[['id', rank]], on='id', how='left')

    df_end = df_end.fillna(0)
    df_end = df_end.astype('int64', errors='ignore')
    df_end = df_end.rename({'id': 'nome_id'}, axis=1)
    df_end.to_csv('novos_arquivos_csv/ibge_ranking.csv', index=0)


def criar_arquivo_freq():
    df_ini = pd.read_csv('novos_arquivos_csv/nomes_censos_ibge_novo.csv', header=0, na_values=0)
    df_nome = pd.read_csv('novos_arquivos_csv/ibge_nomes.csv', header=0, na_values=0)
    df_end = df_nome['id']

    for decada in range(1930, 2020, 10):
        col = 'ate%d' % decada
        freq = 'freq%d' % decada

        df_decada = df_ini[['id', col]]
        df_decada = df_decada.dropna()

        total = df_decada[col].sum()
        df_decada[freq] = (df_decada[col]/total)*100

        df_end = pd.merge(df_end, df_decada[['id', freq]], on='id', how='left')

    df_end = df_end.fillna(0)
    df_end = df_end.rename({'id': 'nome_id'}, axis=1)
    df_end.to_csv('novos_arquivos_csv/ibge_frequencia.csv', index=0)


def criar_completo():
    df_ini = pd.read_csv('novos_arquivos_csv/nomes_censos_ibge_novo.csv', header=0)
    df_rank = pd.read_csv('novos_arquivos_csv/ibge_ranking.csv', header=0)
    df_end = pd.merge(df_ini, df_rank, left_on='id', right_on='nome_id', how='left')
    df_freq = pd.read_csv('novos_arquivos_csv/ibge_frequencia.csv', header=0)
    df_end = pd.merge(df_end, df_freq, left_on='id', right_on='nome_id', how='left')
    df_end = df_end.fillna(0)
    df_end = df_end.drop(['nome_id_x', 'nome_id_y'], axis=1)
    df_end.to_csv('novos_arquivos_csv/ibge_completo.csv', index=0)


criar_arquivo_ibge_nomes()
criar_arquivo_rank()
criar_arquivo_freq()
criar_completo()