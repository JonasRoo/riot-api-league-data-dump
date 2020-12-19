def test_database_setup():
    """
    Test database integrity by initializing session.
    """
    from .session.session_handler import session_scope

    with session_scope() as session:
        pass