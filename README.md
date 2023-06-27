# :zap: **PyBoot**

## :thinking: **Como usar?**

:point_right: Para ver as opções disponíveis, digite:

```console
$ poetry run pyboot --help
```

:point_right: Para criar um arquivo de configuração do PyBoot, basta inserir as opções desejadas para o seu projeto ao executar o CLI. Automaticamente, um arquivo pyboot.toml será gerado no diretório do novo projeto Django.

```console
$ poetry run pyboot -np test_pyboot -pv 3.10.10
```

```console
# Output
02:18:54 General settings completed
02:18:59 Environment settings completed
02:19:00 Django settings completed
name_project = "test_pyboot"
directory = "/path/of/project/blogger"
add_python_version = "3.10.10"

'test_pyboot' configured! 🚀
```

## :warning: **Avisos**

É importante notar a PyBoot está em fase desenvolvimento. Mas se você quiser utilizar mesmo assim, você terá que:

1. Clonar esse repositório e acessar essa branch feature.
2. Ter o Poetry instalado na sua máquina.
3. Instalar todas as dependências do projeto: `poetry install`

:rocket: Pronto, agora é só utilizar a PyBoost com `poetry run pyboot --help`

## :rotating_light: **Licença**

O projeto PyBoot é distribuído sob a licença MIT, saiba mais em [LICENSE](LICENSE).
