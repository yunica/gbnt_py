import click
from migrate import process


@click.command(short_help="Dowload and migrate data")
@click.option(
    "--folder_path",
    help="path for data ",
    type=str,
)
@click.option(
    "--database_db",
    help="database name ",
    envvar="POSTGRES_DB",
    type=str,
)
@click.option(
    "--database_user",
    help="database user ",
    envvar="POSTGRES_USER",
    type=str,
)
@click.option(
    "--database_password",
    help="database password ",
    envvar="POSTGRES_PASSWORD",
    type=str,
)
@click.option(
    "--database_port",
    help="database port ",
    envvar="POSTGRES_PORT",
    type=int,
)
@click.option(
    "--database_host",
    help="database host ",
    default="db",
    type=str,
)
def main(
    folder_path,
    database_db,
    database_user,
    database_password,
    database_port,
    database_host,
):
    process(
        folder_path,
        database_db,
        database_user,
        database_password,
        database_port,
        database_host,
    )


if __name__ == "__main__":
    main()
