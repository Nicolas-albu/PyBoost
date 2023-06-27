# :zap: **PyBoot**

## :thinking: **How ​​to use?**

:point_right: To see the available options, type:

```console
$ poetry run pyboot --help
```

:point_right: To create a PyBoot configuration file, simply enter the desired options for your project when running the CLI. Automatically, a pyboot.toml file will be generated in the new Django project directory.

```console
$ poetry run pyboot -np test_pyboot -pv 3.10.10
```

```console
# Output
02:18:54 General settings completed
02:18:59 Environment settings completed
02:19:00 Django settings completed
name_project = "test_pyboot"
directory="/path/of/project/blogger"
add_python_version="3.10.10"

'test_pyboot' configured! 🚀
```

## :warning: **Warnings**

It's important to note that PyBoot is in the development stage. But if you want to use it anyway, you'll have to:

1. Clone this repository and access this feature branch.
2. Have Poetry installed on your machine.
3. Install all project dependencies: `poetry install`

:rocket: Done, now just use PyBoot with `poetry run pyboot --help`

## :rotating_light: **License**

The PyBoot project is distributed under the MIT license, learn more at [LICENSE](LICENSE).
