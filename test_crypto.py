#!./flask/bin/python

from app import crypto

password = 'dave is the best in the world'
digest = crypto.get_digest(password)

fake_password = 'this is not the right password'

if crypto.is_password(password, digest):
	print("the real password is legit")
else:
	print("opps, the real password isn't legit")

if crypto.is_password(fake_password, digest):
	print("we have a problem! the fake password appears legit")
else:
	print("as you were, fake password is not legit")

