import requests
import hashlib
import sys


def request_api_data(query_params):
    url = 'https://api.pwnedpasswords.com/range/' + query_params
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, Please Try Again!')
    return res
    

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0




def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f"your password: {password} is found {count} times, It's time to change!")
        else:
            print(f'Awesome! You look great')
    return 'Done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))