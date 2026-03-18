#!/usr/bin/env python3
"""
Test RSA Key Generation and Cryptographic Functions
Unit tests for the Computer Security Project
"""

import os
import tempfile
import sys
import base64

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.utils.rsa_key_helper import generate_rsa_key_pair
from modules.utils.file_crypto_helper import encrypt_file_for_user, decrypt_file_for_user
from modules.utils.signature_helper import DigitalSignatureHelper
from Crypto.PublicKey import RSA

def test_rsa_key_generation():
    """Test RSA key pair generation"""
    print("Testing RSA key generation...")
    try:
        private_key_pem, public_key_pem = generate_rsa_key_pair()
        assert private_key_pem is not None, "Private key should not be None"
        assert public_key_pem is not None, "Public key should not be None"
        assert len(private_key_pem) > 0, "Private key should not be empty"
        assert len(public_key_pem) > 0, "Public key should not be empty"

        # Verify keys can be loaded
        private_key = RSA.import_key(private_key_pem)
        public_key = RSA.import_key(public_key_pem)
        assert private_key is not None, "Private key should be loadable"
        assert public_key is not None, "Public key should be loadable"

        print("RSA key generation test passed")
        return True
    except Exception as e:
        print(f"RSA key generation test failed: {e}")
        return False

def test_file_encryption():
    """Test file encryption and decryption"""
    print("Testing file encryption/decryption...")
    try:
        # Generate test keys
        private_key_pem, public_key_pem = generate_rsa_key_pair()

        # Create a temporary test file
        test_data = b"Hello, World! This is a test file for encryption."
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(test_data)
            input_file = f.name

        # Create output file path
        output_file = input_file + '.enc'

        # Encrypt the file
        encrypted_file = encrypt_file_for_user(
            sender_email="test@example.com",
            receiver_pub_pem=public_key_pem,
            input_filepath=input_file,
            output_path=output_file,
            mode="combined"
        )

        # For decryption, we need the decrypted private key (not encrypted)
        # Since we're testing, we'll use the private key directly
        # In real usage, you'd decrypt the stored private key first
        decrypted_output = input_file + '.decrypted'

        decrypt_file_for_user(
            receiver_priv_pem=private_key_pem,
            passphrase="",  # No passphrase for raw PEM
            encrypted_path=encrypted_file,
            output_filepath=decrypted_output
        )

        # Read decrypted file and verify
        with open(decrypted_output, 'rb') as f:
            decrypted_data = f.read()

        assert decrypted_data == test_data, "Decrypted data should match original"

        # Clean up
        os.unlink(input_file)
        os.unlink(encrypted_file)
        os.unlink(decrypted_output)

        print("File encryption/decryption test passed")
        return True
    except Exception as e:
        print(f"File encryption/decryption test failed: {e}")
        return False

def test_digital_signature():
    """Test digital signature creation and verification"""
    print("Testing digital signature...")
    try:
        # Generate test keys
        private_key_pem, public_key_pem = generate_rsa_key_pair()

        # Create a temporary test file
        test_data = b"This is test data for digital signature."
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(test_data)
            test_file = f.name

        # Initialize signature helper
        sig_helper = DigitalSignatureHelper()

        # Sign the file
        sig_file_path, sig_data = sig_helper.sign_file(
            file_path=test_file,
            signer_email="test@example.com",
            private_key_pem=private_key_pem
        )

        # Verify the signature
        is_valid, message = sig_helper.verify_signature(
            file_path=test_file,
            sig_file_path=sig_file_path,
            public_key_pem=public_key_pem
        )

        assert is_valid == True, f"Signature verification should succeed: {message}"

        # Clean up
        os.unlink(test_file)
        if os.path.exists(sig_file_path):
            os.unlink(sig_file_path)

        print("Digital signature test passed")
        return True
    except Exception as e:
        print(f"Digital signature test failed: {e}")
        return False

def run_all_tests():
    """Run all test functions"""
    print("Running RSA Cryptography Tests")
    print("=" * 40)

    tests = [
        test_rsa_key_generation,
        test_file_encryption,
        test_digital_signature
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed!")
        return True
    else:
        print("Some tests failed!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)