# service_loader.py
from .services import registration, login, caregiver, payments, users

def test_imports():
    """
    Simple function to verify all service modules are loaded correctly.
    """
    print("✅ registration module loaded:", registration)
    print("✅ login module loaded:", login)
    print("✅ caregiver module loaded:", caregiver)
    print("✅ payments module loaded:", payments)
    print("✅ users module loaded:", users)
    return "All service modules imported successfully!"
