def test_database_setup():
    from .session.session_handler import session_scope

    with session_scope() as session:
        pass