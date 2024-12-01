from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")


# C_Def: class_name -> Hasher
# C_func: hashes password and verify them for security purposes
class Hasher:

    # method to return the hashed password from the plain password
    @staticmethod
    def get_hashed_password(password):
        hashed_password = pwd_cxt.hash(password)
        return hashed_password

    # method to verify the password after hashing
    @staticmethod
    def verify_password(plain_password,
                        hashed_password):
        return pwd_cxt.verify(plain_password,
                              hashed_password)
