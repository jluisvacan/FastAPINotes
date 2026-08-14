import typer

from app.seeds.service import run_users, run_categories, run_tags, run_all

#typer crea interfaces de linea de comandos
app = typer.Typer(help="Seeds: users, categories, tags")

#app.command define un comando para la interfaz en consola
@app.command("all")
def all_seeds():
    run_all()
    typer.echo("Todos los seeds creados")


@app.command("users")
def users():
    run_users()
    typer.echo("Usuarios cargados")


@app.command("categories")
def categories():
    run_categories()
    typer.echo("Categorias cargadas")


@app.command("tags")
def tags():
    run_tags()
    typer.echo("Tags cargadas")