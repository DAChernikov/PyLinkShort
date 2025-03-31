from app.services.shortener import generate_short_code

def test_generate_short_code_length():
    code = generate_short_code()
    assert isinstance(code, str)
    assert len(code) == 6