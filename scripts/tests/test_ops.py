from scripts.ops.check_notebooks import check, read_files


def test_check_notebooks():
    notebooks, scripts, htmls = read_files()
    has_missing_files, has_proper_naming, has_clean_outputs = check(
        notebooks, scripts, htmls
    )

    assert has_missing_files is False, "Você precisa gerar arquivos .py e .html"
    assert has_proper_naming is True, "Verifique o padrão dos nomes dos notebooks"
    assert has_clean_outputs is True, "Os outputs não estão limpos"
