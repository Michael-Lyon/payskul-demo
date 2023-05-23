import random

def generate_random_credit():
    """Takes no arguments and return a random credit."""

    # Set the minimum and maximum credit limit values
    min_credit_limit = 20_000
    max_credit_limit = 200_000

    return random.randint(min_credit_limit, max_credit_limit)



def validate_national_id(national_id: str) -> bool:
    """Validates a national identity number.

    Args:
        national_id: The national identity number to be validated.

    Returns:
        True if the national identity number is valid, False otherwise.
    """
    if not national_id or len(national_id) != 11:
        return False
    return True
    # # Extract the first 12 digits of the national identity number
    # first_12_digits = national_id[:12]

    # # Calculate the 13th digit using a modulus 11 check
    # check_digit = int(national_id[12])
    # sum_ = sum(int(d) * (13 - i) for i, d in enumerate(first_12_digits))
    # calculated_check_digit = (11 - sum_ % 11) % 11

    # # Check if the calculated check digit matches the original check digit
    # return check_digit == calculated_check_digit


def validate_bvn(bvn: str) -> bool:
    """Validates a bank verification number.

    Args:
        bvn: The bank verification number to be validated.

    Returns:
        True if the bank verification number is valid, False otherwise.
    """
    if not bvn or len(bvn) != 11:
        return False
    
    return True
    # # Extract the first 10 digits of the BVN
    # first_10_digits = bvn[:10]

    # # Calculate the 11th digit using a modulus 11 check
    # check_digit = int(bvn[10])
    # sum_ = sum(int(d) * (11 - i) for i, d in enumerate(first_10_digits))
    # calculated_check_digit = (11 - sum_ % 11) % 11

    # # Check if the calculated check digit matches the original check digit
    # return check_digit == calculated_check_digit



def get_natinal_id():

    # Generate the first 12 digits of the national identity number
    first_12_digits = "01011998" + "".join([str(random.randint(0, 9)) for _ in range(4)])

    # Calculate the check digit
    sum_ = sum(int(d) * (13 - i) for i, d in enumerate(first_12_digits))
    calculated_check_digit = (11 - sum_ % 11) % 11

    # Generate the national identity number
    return first_12_digits + str(calculated_check_digit)


def get_bvn():

    # Generate the first 10 digits of the BVN
    first_10_digits = "01011998" + "".join([str(random.randint(0, 9)) for _ in range(2)])

    # Calculate the check digit
    sum_ = sum(int(d) * (11 - i) for i, d in enumerate(first_10_digits))
    calculated_check_digit = (11 - sum_ % 11) % 11

    # Generate the BVN
    bvn = first_10_digits + str(calculated_check_digit)
    return bvn


if __name__ == "__main__":
    nin = get_natinal_id()
    bvn = get_bvn()

    if validate_national_id(nin):
        print("nin:", nin)
            
    if validate_bvn(bvn):
        print("bvn:", bvn)
