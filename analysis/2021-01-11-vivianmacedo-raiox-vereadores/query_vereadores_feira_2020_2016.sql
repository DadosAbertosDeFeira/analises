---- Query usada para importar os dados via Big Query em https://basedosdados.org/dataset/br-tse-eleicoes/resource/7c47f0e4-c8ef-46fe-a61d-9179e5adab64
SELECT
    *
FROM
    `basedosdados.br_tse_eleicoes.resultados_candidato_municipio` AS r
    LEFT JOIN (
        SELECT
            *
        FROM
            `basedosdados.br_tse_eleicoes.candidatos`
        WHERE
            (
                ano = 2020
                OR ano = 2016
            )
            AND id_municipio_tse = 35157
    ) AS c ON r.numero_candidato = c.numero_candidato
    AND r.ano = c.ano
WHERE
    (
        r.ano = 2020
        OR r.ano = 2016
    )
    AND r.id_municipio_tse = 35157
    AND r.cargo = 'vereador'
