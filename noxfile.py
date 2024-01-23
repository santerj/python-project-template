import nox

@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "$PROJECT")

@nox.session
def test(session):
    session.install("pytest")
    session.run("pytest")
